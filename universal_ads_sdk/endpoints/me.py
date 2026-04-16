"""
Me endpoints for accessing authenticated user's organizations and ad accounts.
"""

from typing import Dict, Any, Optional, List
from ._base import BaseEndpoint


class MeEndpoint(BaseEndpoint):
    """Endpoint for accessing authenticated user's information."""

    def get_organizations(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get all organizations that the authenticated application has organization-level scopes for.

        Args:
            limit: Number of items to retrieve per page (default: 10, max: 100)
            offset: Pagination offset for retrieving the next set of items (default: 0)

        Returns:
            Dictionary containing the list of organizations with pagination
        """
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/me/organizations", params=params)

    def get_adaccounts(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        organization_ids: Optional[List[str]] = None,
        authorization_statuses: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get all ad accounts that the authenticated application has ad account-level or organization-level scopes for.

        Args:
            limit: Number of items to retrieve per page (default: 10, max: 100)
            offset: Pagination offset for retrieving the next set of items (default: 0)
            organization_ids: Optional organization IDs to filter by
            authorization_statuses: Optional authorization status values to filter by

        Returns:
            Dictionary containing the list of ad accounts with pagination
        """
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if organization_ids:
            params["organization_id"] = organization_ids
        if authorization_statuses:
            params["authorization_status"] = authorization_statuses

        return self._make_request("GET", "/me/adaccounts", params=params)
