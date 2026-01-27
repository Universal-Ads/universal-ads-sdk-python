"""
Me endpoints for accessing authenticated user's organizations and ad accounts.
"""

from typing import Dict, Any, Optional
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
    ) -> Dict[str, Any]:
        """
        Get all ad accounts that the authenticated application has ad account-level or organization-level scopes for.

        Args:
            limit: Number of items to retrieve per page (default: 10, max: 100)
            offset: Pagination offset for retrieving the next set of items (default: 0)

        Returns:
            Dictionary containing the list of ad accounts with pagination
        """
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/me/adaccounts", params=params)
