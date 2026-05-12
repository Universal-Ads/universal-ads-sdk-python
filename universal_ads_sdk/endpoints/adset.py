"""
Ad set management endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class AdsetEndpoint(BaseEndpoint):
    """Endpoint for managing ad sets."""

    def get_adsets(
        self,
        adaccount_id: str,
        campaign_ids: Optional[list] = None,
        adset_ids: Optional[list] = None,
        name: Optional[str] = None,
        status: Optional[list] = None,
        include_archived: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of ad sets."""
        params: Dict[str, Any] = {"adaccount_id": adaccount_id}
        if campaign_ids is not None:
            params["campaign_ids"] = campaign_ids
        if adset_ids is not None:
            params["adset_ids"] = adset_ids
        if name is not None:
            params["name"] = name
        if status is not None:
            params["status"] = status
        if include_archived is not None:
            params["include_archived"] = include_archived
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if sort is not None:
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
