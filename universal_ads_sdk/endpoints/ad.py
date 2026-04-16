"""
Ad management endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class AdEndpoint(BaseEndpoint):
    """Endpoint for managing ads."""

    def get_ads(
        self,
        adaccount_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        adset_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of ads."""
        params = {}
        if adaccount_id:
            params["adaccount_id"] = adaccount_id
        if campaign_id:
            params["campaign_id"] = campaign_id
        if adset_id:
            params["adset_id"] = adset_id
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if sort:
            params["sort"] = sort
        params.update(kwargs)

        return self._make_request("GET", "/ad", params=params)

    def get_ad(self, ad_id: str) -> Dict[str, Any]:
        """Get a specific ad by ID."""
        return self._make_request("GET", f"/ad/{ad_id}")

    def create_ad(self, **data) -> Dict[str, Any]:
        """Create a new ad."""
        return self._make_request("POST", "/ad", data=data)

    def update_ad(self, ad_id: str, **data) -> Dict[str, Any]:
        """Update an existing ad."""
        return self._make_request("PUT", f"/ad/{ad_id}", data=data)
