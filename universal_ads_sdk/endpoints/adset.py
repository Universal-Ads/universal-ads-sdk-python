"""
Ad set management endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class AdsetEndpoint(BaseEndpoint):
    """Endpoint for managing ad sets."""

    def get_adsets(
        self,
        adaccount_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of ad sets."""
        params = {}
        if adaccount_id:
            params["adaccount_id"] = adaccount_id
        if campaign_id:
            params["campaign_id"] = campaign_id
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if sort:
            params["sort"] = sort
        params.update(kwargs)

        return self._make_request("GET", "/adset", params=params)

    def get_adset(self, adset_id: str) -> Dict[str, Any]:
        """Get a specific ad set by ID."""
        return self._make_request("GET", f"/adset/{adset_id}")

    def create_adset(self, **data) -> Dict[str, Any]:
        """Create a new ad set."""
        return self._make_request("POST", "/adset", data=data)

    def update_adset(self, adset_id: str, **data) -> Dict[str, Any]:
        """Update an existing ad set."""
        return self._make_request("PUT", f"/adset/{adset_id}", data=data)
