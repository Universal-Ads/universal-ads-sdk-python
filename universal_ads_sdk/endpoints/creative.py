"""
Creative management endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class CreativeEndpoint(BaseEndpoint):
    """Endpoint for managing creatives."""

    def get_creatives(
        self,
        adaccount_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a list of creatives.

        Args:
            adaccount_id: Filter by ad account ID
            limit: Maximum number of results to return
            offset: Number of results to skip
            sort: Sort field and direction (e.g., 'id_asc', 'name_desc')

        Returns:
            Dictionary containing the list of creatives
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

        return self._make_request("GET", "/creative", params=params)

    def get_creative(self, creative_id: str) -> Dict[str, Any]:
        """
        Get a specific creative by ID.

        Args:
            creative_id: The creative ID

        Returns:
            Dictionary containing the creative data
        """
        return self._make_request("GET", f"/creative/{creative_id}")

    def create_creative(
        self, adaccount_id: str, name: str, media_id: str
    ) -> Dict[str, Any]:
        """
        Create a new creative.

        Args:
            adaccount_id: The ad account ID
            name: Creative name
            media_id: The media ID to associate with the creative

        Returns:
            Dictionary containing the created creative data
        """
        data = {"ad_account_id": adaccount_id, "name": name, "media_id": media_id}
        return self._make_request("POST", "/creative", data=data)

    def update_creative(
        self, creative_id: str, name: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing creative.

        Args:
            creative_id: The creative ID to update
            name: New creative name
            **kwargs: Additional fields to update

        Returns:
            Dictionary containing the updated creative data
        """
        data = {}
        if name is not None:
            data["name"] = name
        data.update(kwargs)

        return self._make_request("PUT", f"/creative/{creative_id}", data=data)

    def delete_creative(self, creative_id: str) -> Dict[str, Any]:
        """
        Delete a creative.

        Args:
            creative_id: The creative ID to delete

        Returns:
            Empty dictionary on success
        """
        return self._make_request("DELETE", f"/creative/{creative_id}")
