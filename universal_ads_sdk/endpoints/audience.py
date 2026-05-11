"""
Audience management endpoints.
"""

from typing import Dict, Any, Optional, List
from ._base import BaseEndpoint


class AudienceEndpoint(BaseEndpoint):
    """Endpoint for managing custom audiences."""

    def create_audience(
        self,
        adaccount_id: str,
        name: str,
        segment_type: str,
        media_id: Optional[str] = None,
        users: Optional[List[str]] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new custom audience.

        Args:
            adaccount_id: The ad account ID (UUID)
            name: Audience name (1-255 characters)
            segment_type: Type of audience to create
            media_id: The media ID (UUID) to associate with the audience. Required if users is not provided.
            users: List of user identifiers (emails, IPs, or UUIDs as strings) to include in the audience.
                   Maximum 10,000 users per request. Required if media_id is not provided.
            description: Optional audience description (max 255 characters)

        Returns:
            Dictionary containing the created audience data

        Raises:
            ValueError: If neither media_id nor users is provided, or if users list exceeds 10,000 items
        """
        # Validation: either media_id or users must be provided
        if not media_id and not users:
            raise ValueError("Either media_id or users must be provided")

        # Validation: users list cannot exceed 10,000 items
        if users and len(users) > 10000:
            raise ValueError("Users list cannot exceed 10,000 items")

        data = {
            "adaccount_id": adaccount_id,
            "name": name,
            "segment_type": segment_type,
        }

        if media_id:
            data["media_id"] = media_id

        if users:
            data["users"] = users

        if description is not None:
            data["description"] = description

        return self._make_request("POST", "/audience", data=data)

    def get_audiences(
        self,
        adaccount_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        audience_ids: Optional[List[str]] = None,
        segment_ids: Optional[List[str]] = None,
        segment_type: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a list of custom audiences.

        Args:
            adaccount_id: Filter by ad account ID (UUID)
            name: Filter by audience name
            description: Filter by audience description
            status: Filter by audience status
            audience_ids: List of audience IDs to include (OpenAPI query param)
            segment_ids: Backward-compatible alias for audience_ids
            segment_type: Filter by audience segment type
            limit: Maximum number of results to return
            offset: Number of results to skip
            sort: Sort field and direction (e.g., 'id_asc', 'name_desc')

        Returns:
            Dictionary containing the list of audiences with pagination
        """
        params = {"adaccount_id": adaccount_id}

        if name:
            params["name"] = name
        if description:
            params["description"] = description
        if status:
            params["status"] = status
        # Keep segment_ids alias for payload parity while migrating naming.
        effective_audience_ids = audience_ids or segment_ids
        if effective_audience_ids:
            params["audience_ids"] = effective_audience_ids
        if segment_type:
            params["segment_type"] = segment_type
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if sort:
            params["sort"] = sort

        return self._make_request("GET", "/audience", params=params)

    def get_audience(self, audience_id: str) -> Dict[str, Any]:
        """
        Get a specific audience by ID.

        Args:
            audience_id: The audience ID (UUID)

        Returns:
            Dictionary containing the audience data
        """
        return self._make_request("GET", f"/audience/{audience_id}")

    def update_audience(
        self,
        audience_id: str,
        name: str,
        description: str,
    ) -> Dict[str, Any]:
        """
        Update an existing audience.

        Args:
            audience_id: The audience ID to update (UUID)
            name: New audience name (1-255 characters)
            description: New audience description (max 255 characters)

        Returns:
            Dictionary containing the updated audience data
        """
        data = {"name": name, "description": description}
        return self._make_request("PUT", f"/audience/{audience_id}", data=data)

    def delete_audience(self, audience_id: str) -> Dict[str, Any]:
        """
        Delete an audience.

        Args:
            audience_id: The audience ID to delete (UUID)

        Returns:
            Empty dictionary on success
        """
        return self._make_request("DELETE", f"/audience/{audience_id}")

    def update_audience_users(
        self,
        audience_id: str,
        users: Optional[List[str]] = None,
        media_id: Optional[str] = None,
        remove: bool = False,
    ) -> Dict[str, Any]:
        """
        Add or remove users from an audience using users list or uploaded media.

        Args:
            audience_id: The audience ID (UUID)
            users: Optional list of user identifiers (emails, IPs, or UUIDs as strings).
                   Maximum 10,000 users per request.
            media_id: Optional media ID (UUID) pointing to uploaded audience data.
            remove: If True, removes users from the audience. If False (default), adds users.

        Returns:
            Empty dictionary on success

        Raises:
            ValueError: If neither users nor media_id is provided, or if users list exceeds 10,000 items
        """
        if not users and not media_id:
            raise ValueError("Either users or media_id must be provided")

        if users and len(users) > 10000:
            raise ValueError("Users list cannot exceed 10,000 items")

        data: Dict[str, Any] = {"remove": remove}
        if users:
            data["users"] = users
        if media_id:
            data["media_id"] = media_id

        return self._make_request("PUT", f"/audience/{audience_id}/users", data=data)
