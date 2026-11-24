import base64
import json
import logging
import threading
import time
from unittest.mock import MagicMock

import pytest
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

import universal_ads_sdk
from universal_ads_sdk import (
    APIError,
    AuthenticationError,
    TokenError,
    TokenStoreError,
    UniversalAdsClient,
)

FROZEN = 1700000000.0
ACCESS = "access-token-secret-value"
NEW_ACCESS = "new-access-token-secret-value"
REFRESH = "refresh-token-secret-value"
NEW_REFRESH = "new-refresh-token-secret-value"
SECRET = "client-secret-secret-value"
CLIENT_ID = "client-id-value"
SYSTEM_USER = "system-user-id-value"
PRODUCTION = "https://api.universalads.com/v1"


class FakeResponse:
    def __init__(self, status_code, payload=None, headers=None):
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}
        self.text = ""

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        if self._payload is None:
            raise ValueError("no json")
        return self._payload


def _pem():
    key = ec.generate_private_key(ec.SECP256R1())
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")


def _token_response(
    access_token=NEW_ACCESS,
    expires_in=3600,
    refresh_token=NEW_REFRESH,
    scope="SCOPE_1 SCOPE_2",
    include_refresh=True,
):
    body = {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "scope": scope,
    }
    if include_refresh:
        body["refresh_token"] = refresh_token
    return FakeResponse(200, body)


def _api_ok():
    return FakeResponse(200, {"data": []})


def _refresh_client(**overrides):
    params = {
        "client_id": CLIENT_ID,
        "client_secret": SECRET,
        "refresh_token": REFRESH,
        "store_hook": lambda **kwargs: None,
    }
    params.update(overrides)
    return UniversalAdsClient(**params)


def _attach_api(client, response=None):
    client.session.request = MagicMock(return_value=response or _api_ok())
    return client.session.request


@pytest.fixture
def frozen_time(monkeypatch):
    monkeypatch.setattr("universal_ads_sdk.client.time.time", lambda: FROZEN)


@pytest.fixture
def post(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("universal_ads_sdk.client.requests.post", mock)
    return mock


def test_signed_client_still_signs(post):
    client = UniversalAdsClient("api-key-value", _pem())
    api = _attach_api(client)

    client.get_organizations()

    post.assert_not_called()
    headers = api.call_args.kwargs["headers"]
    assert headers["x-api-key"] == "api-key-value"
    assert headers["x-timestamp"]
    assert headers["x-signature"]
    assert headers["x-sdk-version"] == universal_ads_sdk.__version__
    assert headers["x-sdk-source"] == "universal-ads-python-sdk"
    assert "Authorization" not in headers


def test_signed_client_rejects_signing_headers_and_allows_authorization():
    pem = _pem()
    with pytest.raises(ValueError, match="x-api-key"):
        UniversalAdsClient("api-key-value", pem, headers={"x-api-key": "other"})

    client = UniversalAdsClient(
        "api-key-value",
        pem,
        headers={"Authorization": "Bearer caller-supplied"},
    )
    api = _attach_api(client)
    client.get_organizations()
    assert api.call_args.kwargs["headers"]["Authorization"] == "Bearer caller-supplied"
    assert "x-signature" in api.call_args.kwargs["headers"]


def test_api_key_with_refresh_token_raises_before_any_request(post):
    with pytest.raises(ValueError, match="cannot be combined") as exc:
        UniversalAdsClient(api_key="api-key-value", refresh_token=REFRESH)
    assert REFRESH not in str(exc.value)
    with pytest.raises(ValueError, match="cannot be combined"):
        UniversalAdsClient("api-key-value", "not-a-pem", refresh_token=REFRESH)
    post.assert_not_called()


def test_bad_signing_key_is_an_authentication_error():
    with pytest.raises(AuthenticationError):
        UniversalAdsClient("api-key-value", "not-a-pem")


def test_token_client_rejects_authorization_header():
    with pytest.raises(ValueError, match="Authorization"):
        UniversalAdsClient(
            access_token=ACCESS,
            headers={"Authorization": f"Bearer {ACCESS}"},
        )
    with pytest.raises(ValueError, match="authorization"):
        UniversalAdsClient(
            access_token=ACCESS,
            headers={"authorization": f"Bearer {ACCESS}"},
        )
    with pytest.raises(ValueError, match="x-signature"):
        UniversalAdsClient(access_token=ACCESS, headers={"x-signature": "sig"})


def test_refresh_client_requires_store_hook_and_the_access_token_pair():
    with pytest.raises(ValueError, match="store_hook"):
        UniversalAdsClient(
            client_id=CLIENT_ID,
            client_secret=SECRET,
            refresh_token=REFRESH,
        )
    with pytest.raises(ValueError, match="provided together"):
        _refresh_client(access_token=ACCESS)
    with pytest.raises(ValueError, match="provided together"):
        _refresh_client(access_token_expires_at=FROZEN + 120)
    with pytest.raises(ValueError, match="non-empty string"):
        _refresh_client(client_secret="")


def test_refresh_without_access_token_stores_before_the_call(post, frozen_time):
    order = []

    def hook(**kwargs):
        order.append(("hook", kwargs))

    def send(*args, **kwargs):
        order.append("token")
        return _token_response()

    post.side_effect = send
    client = _refresh_client(store_hook=hook)
    api = _attach_api(client)
    api.side_effect = lambda *args, **kwargs: order.append("api") or _api_ok()

    assert client.get_organizations() == {"data": []}
    assert [step if isinstance(step, str) else step[0] for step in order] == [
        "token",
        "hook",
        "api",
    ]
    assert order[1][1] == {
        "access_token": NEW_ACCESS,
        "expires_at": FROZEN + 3600,
        "refresh_token": NEW_REFRESH,
        "scope": "SCOPE_1 SCOPE_2",
    }
    assert client.access_token == NEW_ACCESS
    assert client.refresh_token == NEW_REFRESH
    assert client.access_token_expires_at == FROZEN + 3600
    assert client.scope == "SCOPE_1 SCOPE_2"
    token_call = post.call_args.kwargs
    assert token_call["url"] == PRODUCTION + "/oauth/token"
    assert token_call["data"] == {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH,
    }
    assert token_call["auth"] == (CLIENT_ID, SECRET)
    assert token_call["allow_redirects"] is False
    assert "headers" not in token_call
    sent = api.call_args.kwargs["headers"]
    assert sent["Authorization"] == f"Bearer {NEW_ACCESS}"
    assert sent["x-sdk-version"] == universal_ads_sdk.__version__
    assert sent["x-sdk-source"] == "universal-ads-python-sdk"

    client.get_organizations()
    assert post.call_count == 1


def test_hook_failure_skips_the_call_and_retries_the_same_tokens(post, frozen_time):
    calls = []

    def hook(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise RuntimeError("disk full")

    post.return_value = _token_response()
    client = _refresh_client(store_hook=hook)
    api = _attach_api(client)

    with pytest.raises(TokenStoreError) as exc:
        client.get_organizations()

    assert isinstance(exc.value.__cause__, RuntimeError)
    assert "disk full" not in str(exc.value)
    assert api.call_count == 0
    assert post.call_count == 1
    assert client.access_token == NEW_ACCESS
    assert client.refresh_token == NEW_REFRESH
    assert client.access_token_expires_at == FROZEN + 3600
    assert client.scope == "SCOPE_1 SCOPE_2"

    client.get_organizations()

    assert post.call_count == 1
    assert api.call_count == 1
    assert calls[0] == calls[1]


def test_hook_success_refreshes_again_when_the_token_is_inside_the_window(
    post, frozen_time
):
    calls = []
    renewed = "renewed-access-token-secret-value"
    renewed_refresh = "renewed-refresh-token-secret-value"

    def hook(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise RuntimeError("disk full")

    post.side_effect = [
        _token_response(expires_in=30),
        _token_response(access_token=renewed, refresh_token=renewed_refresh),
    ]
    client = _refresh_client(store_hook=hook)
    api = _attach_api(client)

    with pytest.raises(TokenStoreError):
        client.get_organizations()

    assert post.call_count == 1
    assert api.call_count == 0

    client.get_organizations()

    assert post.call_count == 2
    assert calls[1]["access_token"] == NEW_ACCESS
    assert calls[1]["refresh_token"] == NEW_REFRESH
    assert calls[2]["access_token"] == renewed
    assert calls[2]["refresh_token"] == renewed_refresh
    assert api.call_args.kwargs["headers"]["Authorization"] == f"Bearer {renewed}"


def test_a_short_follow_up_token_does_not_refresh_again(post, frozen_time):
    calls = []

    def hook(**kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise RuntimeError("disk full")

    post.return_value = _token_response(expires_in=30)
    client = _refresh_client(store_hook=hook)
    api = _attach_api(client)

    with pytest.raises(TokenStoreError):
        client.get_organizations()

    client.get_organizations()

    assert post.call_count == 2
    assert api.call_count == 1
    assert len(calls) == 3


def test_access_token_with_more_than_a_minute_left_is_sent_as_is(post, frozen_time):
    client = _refresh_client(
        access_token=ACCESS,
        access_token_expires_at=FROZEN + 61,
    )
    api = _attach_api(client)

    client.get_organizations()

    post.assert_not_called()
    assert api.call_args.kwargs["headers"]["Authorization"] == f"Bearer {ACCESS}"


def test_access_token_with_a_minute_or_less_left_is_refreshed(post, frozen_time):
    post.return_value = _token_response()
    client = _refresh_client(
        access_token=ACCESS,
        access_token_expires_at=FROZEN + 60,
    )
    api = _attach_api(client)

    client.get_organizations()

    assert post.call_count == 1
    assert api.call_args.kwargs["headers"]["Authorization"] == f"Bearer {NEW_ACCESS}"


def test_token_expiry_is_not_read_from_the_token(post, frozen_time):
    header = base64.urlsafe_b64encode(json.dumps({"alg": "none"}).encode()).decode()
    payload = base64.urlsafe_b64encode(json.dumps({"exp": 1}).encode()).decode()
    jwt_token = f"{header.rstrip('=')}.{payload.rstrip('=')}.sig"
    client = _refresh_client(
        access_token=jwt_token,
        access_token_expires_at=FROZEN + 120,
    )
    api = _attach_api(client)

    client.get_organizations()

    post.assert_not_called()
    assert api.call_args.kwargs["headers"]["Authorization"] == f"Bearer {jwt_token}"


def test_system_user_requests_a_token_without_scope_then_calls(post, frozen_time):
    post.return_value = _token_response(include_refresh=False, expires_in=30)
    client = UniversalAdsClient(
        client_id=CLIENT_ID,
        client_secret=SECRET,
        system_user_id=SYSTEM_USER,
    )
    api = _attach_api(client)

    client.get_organizations()
    client.get_organizations()

    assert post.call_count == 2
    first = post.call_args_list[0].kwargs
    assert first["url"] == PRODUCTION + "/oauth/token"
    assert first["data"] == {
        "grant_type": "client_credentials",
        "system_user_id": SYSTEM_USER,
    }
    assert "scope" not in first["data"]
    assert "refresh_token" not in first["data"]
    assert first["auth"] == (CLIENT_ID, SECRET)
    assert first["allow_redirects"] is False
    assert "headers" not in first
    assert client.refresh_token is None
    sent = api.call_args.kwargs["headers"]
    assert sent["Authorization"] == f"Bearer {NEW_ACCESS}"
    assert sent["x-sdk-version"] == universal_ads_sdk.__version__
    assert sent["x-sdk-source"] == "universal-ads-python-sdk"
    assert "x-api-key" not in sent


def test_system_user_client_rejects_a_store_hook():
    with pytest.raises(ValueError, match="system_user_id"):
        UniversalAdsClient(
            client_id=CLIENT_ID,
            client_secret=SECRET,
            system_user_id=SYSTEM_USER,
            store_hook=lambda **kwargs: None,
        )


def test_system_user_client_rejects_a_stored_access_token():
    with pytest.raises(ValueError, match="system_user_id"):
        UniversalAdsClient(
            client_id=CLIENT_ID,
            client_secret=SECRET,
            system_user_id=SYSTEM_USER,
            access_token=ACCESS,
            access_token_expires_at=FROZEN + 120,
        )


def test_system_user_reuses_a_token_with_more_than_a_minute_left(post, frozen_time):
    post.return_value = _token_response(include_refresh=False, expires_in=61)
    client = UniversalAdsClient(
        client_id=CLIENT_ID,
        client_secret=SECRET,
        system_user_id=SYSTEM_USER,
    )
    api = _attach_api(client)

    client.get_organizations()
    client.get_organizations()

    assert post.call_count == 1
    assert api.call_count == 2
    assert api.call_args.kwargs["headers"]["Authorization"] == f"Bearer {NEW_ACCESS}"


def test_access_token_client_never_calls_the_token_endpoint(post):
    client = UniversalAdsClient(access_token=ACCESS)
    api = _attach_api(client)

    client.get_organizations()
    api.return_value = FakeResponse(401, {"detail": "Invalid or expired token"})
    with pytest.raises(APIError) as exc:
        client.get_organizations()

    assert exc.value.status_code == 401
    assert not isinstance(exc.value, TokenError)
    post.assert_not_called()
    with pytest.raises(ValueError, match="access token alone"):
        UniversalAdsClient(access_token=ACCESS, access_token_expires_at=FROZEN)


def test_invalid_grant_is_a_token_error(post, frozen_time):
    post.return_value = FakeResponse(
        400,
        {"error": "invalid_grant", "error_description": "revoked"},
    )
    client = _refresh_client()
    api = _attach_api(client)

    with pytest.raises(TokenError) as exc:
        client.get_organizations()

    err = exc.value
    assert not isinstance(err, APIError)
    assert err.status_code == 400
    assert err.error == "invalid_grant"
    assert err.error_description == "revoked"
    assert "HTTP 400: invalid_grant: revoked" == str(err)
    api.assert_not_called()


def test_token_endpoint_redirect_is_not_followed(post, frozen_time):
    post.return_value = FakeResponse(
        302,
        ValueError("html"),
        headers={"Location": "https://evil.example/steal"},
    )
    client = _refresh_client()
    api = _attach_api(client)

    with pytest.raises(TokenError) as exc:
        client.get_organizations()

    assert exc.value.status_code == 302
    assert post.call_count == 1
    assert post.call_args.kwargs["url"] == PRODUCTION + "/oauth/token"
    assert post.call_args.kwargs["allow_redirects"] is False
    api.assert_not_called()


def test_unreadable_token_body_is_a_token_error(post, frozen_time):
    post.return_value = FakeResponse(
        200,
        {"access_token": NEW_ACCESS, "expires_in": "3600"},
    )
    client = _refresh_client()
    api = _attach_api(client)

    with pytest.raises(TokenError) as exc:
        client.get_organizations()

    assert exc.value.status_code == 200
    assert NEW_ACCESS not in str(exc.value)
    assert client.refresh_token == REFRESH
    assert client.access_token is None
    api.assert_not_called()


def test_token_server_error_is_not_retried(post, frozen_time):
    post.return_value = FakeResponse(500, {"error": "server_error"})
    client = _refresh_client()
    api = _attach_api(client)

    with pytest.raises(TokenError) as exc:
        client.get_organizations()

    assert exc.value.status_code == 500
    assert exc.value.error == "server_error"
    assert post.call_count == 1
    api.assert_not_called()


def test_token_timeout_is_a_token_error_without_a_status(post, frozen_time):
    post.side_effect = requests.Timeout("timed out")
    client = _refresh_client()

    with pytest.raises(TokenError) as exc:
        client.get_organizations()

    assert exc.value.status_code is None
    assert str(exc.value) == "Token request failed"
    assert isinstance(exc.value.__cause__, requests.Timeout)
    assert SECRET not in str(exc.value)
    assert REFRESH not in str(exc.value)


def test_api_401_and_403_do_not_request_a_token(post, frozen_time):
    client = _refresh_client(
        access_token=ACCESS,
        access_token_expires_at=FROZEN + 3600,
    )
    api = _attach_api(client, FakeResponse(401, {"detail": "Invalid or expired token"}))

    with pytest.raises(APIError) as denied:
        client.get_organizations()

    assert denied.value.status_code == 401
    post.assert_not_called()

    api.return_value = FakeResponse(403, {"error_code": "forbidden"})
    with pytest.raises(APIError) as forbidden:
        client.get_organizations()

    assert forbidden.value.status_code == 403
    post.assert_not_called()


def test_api_403_after_a_scheduled_refresh_does_not_refresh_again(post, frozen_time):
    post.return_value = _token_response()
    client = _refresh_client(
        access_token=ACCESS,
        access_token_expires_at=FROZEN + 30,
    )
    api = _attach_api(client, FakeResponse(403, {"error_code": "forbidden"}))

    with pytest.raises(APIError) as exc:
        client.get_organizations()

    assert exc.value.status_code == 403
    assert post.call_count == 1


def test_threads_sharing_one_refresh_client_request_one_token(post, frozen_time):
    ready = threading.Barrier(2)
    first_entered = threading.Event()
    release = threading.Event()
    errors = []

    def token_post(**kwargs):
        first_entered.set()
        assert release.wait(timeout=2)
        return _token_response()

    post.side_effect = token_post
    client = _refresh_client()
    _attach_api(client)

    def call():
        ready.wait(timeout=2)
        try:
            client.get_organizations()
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=call) for _ in range(2)]
    for thread in threads:
        thread.start()
    assert first_entered.wait(timeout=2)
    try:
        deadline = time.monotonic() + 0.3
        while time.monotonic() < deadline and post.call_count < 2:
            time.sleep(0.01)
        assert post.call_count == 1
    finally:
        release.set()
    for thread in threads:
        thread.join(timeout=2)
        assert not thread.is_alive()
    assert errors == []
    assert post.call_count == 1


def test_non_positive_or_non_finite_expires_in_is_unreadable(post, frozen_time):
    client = _refresh_client(
        access_token=ACCESS,
        access_token_expires_at=FROZEN + 10,
    )
    _attach_api(client)

    for expires_in in (0, -1, float("nan"), float("inf")):
        post.return_value = _token_response(expires_in=expires_in)
        with pytest.raises(TokenError, match="unreadable"):
            client.get_organizations()
        assert client.access_token == ACCESS
        assert client.refresh_token == REFRESH

    assert post.call_count == 4


def test_non_production_base_url_is_used_for_the_token_request(post, frozen_time):
    post.return_value = _token_response()
    base_url = "https://staging-api.universalads.com/v1"
    client = _refresh_client(base_url=base_url)
    _attach_api(client)

    client.get_organizations()

    assert post.call_args.kwargs["url"] == base_url + "/oauth/token"

    slashed = _refresh_client(base_url=base_url + "/")
    _attach_api(slashed)
    slashed.get_organizations()
    assert post.call_args.kwargs["url"] == base_url + "/oauth/token"


def test_repr_and_token_error_omit_secrets(post, frozen_time, caplog):
    caplog.set_level(logging.DEBUG)
    post.return_value = FakeResponse(
        400,
        {"error": "invalid_grant", "error_description": "revoked"},
    )
    client = _refresh_client(
        access_token=ACCESS,
        access_token_expires_at=FROZEN + 10,
    )

    with pytest.raises(TokenError) as exc:
        client.get_organizations()

    basic = base64.b64encode(f"{CLIENT_ID}:{SECRET}".encode()).decode()
    blobs = [repr(client), str(exc.value), repr(exc.value), caplog.text]
    for secret in (
        ACCESS,
        REFRESH,
        SECRET,
        f"Bearer {ACCESS}",
        f"Basic {basic}",
        basic,
    ):
        for blob in blobs:
            assert secret not in blob
