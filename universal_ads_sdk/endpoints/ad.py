"""
Ad management endpoints.
"""

from typing import Any, Dict, Optional

from ._base import BaseEndpoint


class AdEndpoint(BaseEndpoint):
    """Endpoint for managing ads."""

    def get_ads(
        self,
        adaccount_id: str,
        campaign_ids: Optional[list] = None,
        adset_ids: Optional[list] = None,
        ad_ids: Optional[list] = None,
        status: Optional[list] = None,
        include_archived: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of ads."""
        params: Dict[str, Any] = {"adaccount_id": adaccount_id}
        if campaign_ids is not None:
            params["campaign_ids"] = campaign_ids
        if adset_ids is not None:
            params["adset_ids"] = adset_ids
        if ad_ids is not None:
            params["ad_ids"] = ad_ids
        if status is not None:
            params["status"] = status
        if include_archived is not None:
            params["include_archived"] = include_archived
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
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

    def archive_ad(self, ad_id: str) -> Dict[str, Any]:
        """Start async single-ad archive. No JSON body."""
        return self._make_request("POST", f"/ad/{ad_id}/archive", data=None)

    def unarchive_ad(self, ad_id: str) -> Dict[str, Any]:
        """Start async single-ad unarchive. No JSON body."""
        return self._make_request("POST", f"/ad/{ad_id}/unarchive", data=None)
