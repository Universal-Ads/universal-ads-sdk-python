from __future__ import annotations

from unittest.mock import Mock
from urllib.parse import parse_qs, urlparse

import pytest

import universal_ads_sdk.client as client_module
from universal_ads_sdk.client import UniversalAdsClient
from universal_ads_sdk.endpoints.ad import AdEndpoint
from universal_ads_sdk.endpoints.adset import AdsetEndpoint
from universal_ads_sdk.endpoints.campaign import CampaignEndpoint
from universal_ads_sdk.endpoints.pixel import PixelEndpoint


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


def _build_client(monkeypatch: pytest.MonkeyPatch) -> UniversalAdsClient:
    monkeypatch.setattr(client_module, "Authenticator", _FakeAuthenticator)
    return UniversalAdsClient(
        api_key="test-api-key",
        private_key_pem="test-private-key",
    )


def test_client_list_methods_require_adaccount_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = _build_client(monkeypatch)
    with pytest.raises(TypeError):
        client.get_campaigns()
    with pytest.raises(TypeError):
        client.get_adsets()
    with pytest.raises(TypeError):
        client.get_ads()
    with pytest.raises(TypeError):
        client.get_pixels()


def test_campaign_endpoint_uses_spec_filter_params() -> None:
    captured: dict = {}

    def make_request(method: str, endpoint: str, **kwargs):
        captured["method"] = method
        captured["endpoint"] = endpoint
        captured["params"] = kwargs["params"]
        return {}

    endpoint = CampaignEndpoint(make_request)
    endpoint.get_campaigns(
        adaccount_id="acc-1",
        campaign_ids=["cmp-1", "cmp-2"],
        name="Campaign Name",
        status="active",
        campaign_type="performance",
        include_archived=False,
        limit=25,
        offset=0,
        sort="id_asc",
    )

    assert captured["method"] == "GET"
    assert captured["endpoint"] == "/campaign"
    assert captured["params"]["adaccount_id"] == "acc-1"
    assert captured["params"]["campaign_ids"] == ["cmp-1", "cmp-2"]
    assert captured["params"]["offset"] == 0


def test_adset_and_ad_endpoints_forward_list_filters() -> None:
    adset_calls: list[dict] = []
    ad_calls: list[dict] = []

    def adset_request(method: str, endpoint: str, **kwargs):
        adset_calls.append(kwargs["params"])
        return {}

    def ad_request(method: str, endpoint: str, **kwargs):
        ad_calls.append(kwargs["params"])
        return {}

    adset = AdsetEndpoint(adset_request)
    adset.get_adsets(
        adaccount_id="acc-1",
        campaign_ids=["cmp-1"],
        adset_ids=["ads-1"],
        status=["active", "paused"],
        include_archived=False,
        offset=0,
    )

    ad = AdEndpoint(ad_request)
    ad.get_ads(
        adaccount_id="acc-1",
        campaign_ids=["cmp-1"],
        adset_ids=["ads-1"],
        ad_ids=["ad-1"],
        status=["active"],
        include_archived=False,
        offset=0,
    )

    assert adset_calls[0]["campaign_ids"] == ["cmp-1"]
    assert adset_calls[0]["adset_ids"] == ["ads-1"]
    assert adset_calls[0]["offset"] == 0
    assert ad_calls[0]["campaign_ids"] == ["cmp-1"]
    assert ad_calls[0]["ad_ids"] == ["ad-1"]
    assert "sort" not in ad_calls[0]


def test_pixel_endpoint_keeps_minimal_params() -> None:
    calls: list[dict] = []

    def make_request(method: str, endpoint: str, **kwargs):
        calls.append(kwargs["params"])
        return {}

    endpoint = PixelEndpoint(make_request)
    endpoint.get_pixels(adaccount_id="acc-1", limit=10, offset=0)

    assert calls[0] == {"adaccount_id": "acc-1", "limit": 10, "offset": 0}


def test_client_encodes_list_filters_as_repeated_query_params(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = _build_client(monkeypatch)
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    client.session.request = Mock(return_value=mock_response)

    client.get_ads(
        adaccount_id="acc-1",
        campaign_ids=["cmp-1", "cmp-2"],
        adset_ids=["ads-1", "ads-2"],
        ad_ids=["ad-1", "ad-2"],
        status=["active", "paused"],
        include_archived=False,
        offset=0,
    )

    requested_url = client.session.request.call_args.kwargs["url"]
    parsed = parse_qs(urlparse(requested_url).query, keep_blank_values=True)

    assert parsed["adaccount_id"] == ["acc-1"]
    assert parsed["campaign_ids"] == ["cmp-1", "cmp-2"]
    assert parsed["adset_ids"] == ["ads-1", "ads-2"]
    assert parsed["ad_ids"] == ["ad-1", "ad-2"]
    assert parsed["status"] == ["active", "paused"]
    assert parsed["offset"] == ["0"]
    assert parsed["include_archived"] == ["False"]
