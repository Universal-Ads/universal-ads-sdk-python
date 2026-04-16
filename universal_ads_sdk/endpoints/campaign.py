"""
Campaign management endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class CampaignEndpoint(BaseEndpoint):
    """Endpoint for managing campaigns."""

    def get_campaigns(
        self,
        adaccount_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Get a list of campaigns.

        Args:
            adaccount_id: Filter by ad account ID
            limit: Maximum number of results to return
            offset: Number of results to skip
            sort: Sort field and direction
            **kwargs: Additional query params

        Returns:
            Dictionary containing campaign list data
        """
        params = {}
        if adaccount_id:
            params["adaccount_id"] = adaccount_id
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if sort:
            params["sort"] = sort
        params.update(kwargs)

        return self._make_request("GET", "/campaign", params=params)

    def get_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Get a specific campaign by ID."""
        return self._make_request("GET", f"/campaign/{campaign_id}")

    def create_campaign(self, **data) -> Dict[str, Any]:
        """
        Create a new campaign.

        Args:
            **data: Campaign payload fields

        Returns:
            Dictionary containing created campaign data
        """
        return self._make_request("POST", "/campaign", data=data)

    def update_campaign(self, campaign_id: str, **data) -> Dict[str, Any]:
        """
        Update an existing campaign.

        Args:
            campaign_id: The campaign ID to update
            **data: Campaign fields to update

        Returns:
            Dictionary containing updated campaign data
        """
        return self._make_request("PUT", f"/campaign/{campaign_id}", data=data)
