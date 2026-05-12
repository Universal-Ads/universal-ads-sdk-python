from __future__ import annotations

import pytest

from universal_ads_sdk.endpoints.campaign import CampaignEndpoint


def test_create_campaign_allows_web_conversions() -> None:
    requests: list[tuple[str, str, dict]] = []

    def make_request(method: str, endpoint: str, **kwargs):
        requests.append((method, endpoint, kwargs))
        return {"id": "campaign-1"}

    endpoint = CampaignEndpoint(make_request)
    response = endpoint.create_campaign(
        adaccount_id="account-id",
        name="Campaign Name",
        objective="web_conversions",
    )

    assert response["id"] == "campaign-1"
    assert requests[0][0] == "POST"
    assert requests[0][1] == "/campaign"
    assert requests[0][2]["data"]["objective"] == "web_conversions"


def test_create_campaign_rejects_legacy_conversions_objective() -> None:
    endpoint = CampaignEndpoint(lambda *_args, **_kwargs: {})

    with pytest.raises(ValueError, match="Use 'web_conversions' instead"):
        endpoint.create_campaign(
            adaccount_id="account-id",
            name="Campaign Name",
            objective="conversions",
        )


def test_update_campaign_rejects_legacy_conversions_objective() -> None:
    endpoint = CampaignEndpoint(lambda *_args, **_kwargs: {})

    with pytest.raises(ValueError, match="Use 'web_conversions' instead"):
        endpoint.update_campaign("campaign-1", objective="conversions")


def test_create_campaign_keeps_other_objectives_unchanged() -> None:
    requests: list[dict] = []

    def make_request(method: str, endpoint: str, **kwargs):
        requests.append({"method": method, "endpoint": endpoint, "kwargs": kwargs})
        return {"id": "campaign-1"}

    endpoint = CampaignEndpoint(make_request)
    endpoint.create_campaign(
        adaccount_id="account-id",
        name="Awareness Campaign",
        objective="awareness",
    )

    assert requests[0]["kwargs"]["data"]["objective"] == "awareness"
