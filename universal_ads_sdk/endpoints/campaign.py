"""
Campaign management endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class CampaignEndpoint(BaseEndpoint):
    """Endpoint for managing campaigns."""

    @staticmethod
    def _validate_objective(data: Dict[str, Any]) -> None:
        """Validate campaign objective values before request submission."""
        objective = data.get("objective")
        if objective == "conversions":
            raise ValueError(
                "Campaign objective 'conversions' is no longer supported. "
                "Use 'web_conversions' instead."
            )

    def get_campaigns(
        self,
        adaccount_id: str,
        campaign_ids: Optional[list] = None,
        name: Optional[str] = None,
        status: Optional[str] = None,
        campaign_type: Optional[str] = None,
        include_archived: Optional[bool] = None,
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
        params: Dict[str, Any] = {"adaccount_id": adaccount_id}
        if campaign_ids is not None:
            params["campaign_ids"] = campaign_ids
        if name is not None:
            params["name"] = name
        if status is not None:
            params["status"] = status
        if campaign_type is not None:
            params["campaign_type"] = campaign_type
        if include_archived is not None:
            params["include_archived"] = include_archived
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if sort is not None:
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
        self._validate_objective(data)
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
        self._validate_objective(data)
        return self._make_request("PUT", f"/campaign/{campaign_id}", data=data)
