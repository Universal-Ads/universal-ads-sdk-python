from __future__ import annotations

from unittest.mock import Mock

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

import universal_ads_sdk.client as client_module
from universal_ads_sdk import __version__
from universal_ads_sdk.auth import Authenticator
from universal_ads_sdk.client import UniversalAdsClient


class _FakeAuthenticator:
    def __init__(self, api_key: str, private_key_pem: str):
        self.api_key = api_key
        self.private_key_pem = private_key_pem

    def get_auth_headers(self, method: str, url: str, body_str: str):
        return {
            "x-api-key": "auth-key",
            "x-timestamp": "1234567890",
            "x-signature": "signed",
        }


def _build_client(
    monkeypatch: pytest.MonkeyPatch, headers: dict[str, str] | None = None
) -> UniversalAdsClient:
    monkeypatch.setattr(client_module, "Authenticator", _FakeAuthenticator)
    return UniversalAdsClient(
        api_key="test-api-key",
        private_key_pem="test-private-key",
        headers=headers,
    )


def test_client_headers_are_included_on_request(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _build_client(
        monkeypatch,
        headers={"x-ua-client": "mcp", "x-ua-mcp-version": "0.2.0"},
    )

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    client.session.request = Mock(return_value=mock_response)

    client._make_request("GET", "/audience")

    sent_headers = client.session.request.call_args.kwargs["headers"]
    assert sent_headers["x-ua-client"] == "mcp"
    assert sent_headers["x-ua-mcp-version"] == "0.2.0"
    assert sent_headers["x-api-key"] == "auth-key"


def test_content_type_header_is_not_overridden(monkeypatch: pytest.MonkeyPatch) -> None:
    client = _build_client(monkeypatch, headers={"Content-Type": "text/plain"})

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    client.session.request = Mock(return_value=mock_response)

    client._make_request("POST", "/audience", data={"name": "test"})

    sent_headers = client.session.request.call_args.kwargs["headers"]
    assert sent_headers["Content-Type"] == "application/json"


@pytest.mark.parametrize("header_name", ["x-api-key", "x-timestamp", "x-signature"])
def test_reserved_auth_headers_cannot_be_overridden(
    monkeypatch: pytest.MonkeyPatch, header_name: str
) -> None:
    with pytest.raises(
        ValueError, match="cannot override SDK authentication headers"
    ):
        _build_client(monkeypatch, headers={header_name: "override"})


def test_auth_headers_include_current_sdk_version() -> None:
    private_key = ec.generate_private_key(ec.SECP256R1())
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    authenticator = Authenticator(api_key="test-api-key", private_key_pem=private_key_pem)
    headers = authenticator.get_auth_headers("GET", "https://api.universalads.com/v1/me")

    assert headers["x-sdk-version"] == __version__
