"""
Segment management endpoints.
"""

from typing import Dict, Any, Optional, List
from ._base import BaseEndpoint


class SegmentEndpoint(BaseEndpoint):
    """Endpoint for managing custom segments."""

    def create_segment(
        self,
        adaccount_id: str,
        media_id: str,
        name: str,
        segment_type: str,
        description: Optional[str] = None,
        large_files: bool = False,
    ) -> Dict[str, Any]:
        """
        Create a new custom segment.

        Args:
            adaccount_id: The ad account ID (UUID)
            media_id: The media ID (UUID) to associate with the segment
            name: Segment name (1-255 characters)
            segment_type: Type of segment to create
            description: Optional segment description (max 255 characters)
            large_files: Whether to use large files processing (default: False)

        Returns:
            Dictionary containing the created segment data
        """
        data = {
            "adaccount_id": adaccount_id,
            "media_id": media_id,
            "name": name,
            "segment_type": segment_type,
            "large_files": large_files,
        }
        if description is not None:
            data["description"] = description

        return self._make_request("POST", "/segment", data=data)

    def get_segments(
        self,
        adaccount_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        segment_ids: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get a list of custom segments.

        Args:
            adaccount_id: Filter by ad account ID (UUID)
            name: Filter by segment name
            description: Filter by segment description
            status: Filter by segment status (e.g., active, inactive)
            segment_ids: List of segment IDs to include (UUIDs)
            limit: Maximum number of results to return
            offset: Number of results to skip
            sort: Sort field and direction (e.g., 'id_asc', 'name_desc')

        Returns:
            Dictionary containing the list of segments with pagination
        """
        params = {"adaccount_id": adaccount_id}

        if name:
            params["name"] = name
        if description:
            params["description"] = description
        if status:
            params["status"] = status
        if segment_ids:
            params["segment_ids"] = segment_ids
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if sort:
            params["sort"] = sort

        return self._make_request("GET", "/segment", params=params)

    def get_segment(self, segment_id: str) -> Dict[str, Any]:
        """
        Get a specific segment by ID.

        Args:
            segment_id: The segment ID (UUID)

        Returns:
            Dictionary containing the segment data
        """
        return self._make_request("GET", f"/segment/{segment_id}")

    def update_segment(
        self,
        segment_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing segment.

        Args:
            segment_id: The segment ID to update (UUID)
            name: New segment name (1-255 characters)
            description: New segment description (max 255 characters)

        Returns:
            Dictionary containing the updated segment data
        """
        data = {"name": name}
        if description is not None:
            data["description"] = description

        return self._make_request("PUT", f"/segment/{segment_id}", data=data)

    def delete_segment(self, segment_id: str) -> Dict[str, Any]:
        """
        Delete a segment.

        Args:
            segment_id: The segment ID to delete (UUID)

        Returns:
            Empty dictionary on success
        """
        return self._make_request("DELETE", f"/segment/{segment_id}")

    def extend_segment(
        self,
        segment_id: str,
        media_id: str,
        large_files: bool = False,
    ) -> Dict[str, Any]:
        """
        Extend a segment with additional media.

        Args:
            segment_id: The segment ID to extend (UUID)
            media_id: The media ID (UUID) to add to the segment
            large_files: Whether to use large files processing (default: False)

        Returns:
            Empty dictionary on success
        """
        data = {
            "media_id": media_id,
            "large_files": large_files,
        }

        return self._make_request("POST", f"/segment/{segment_id}/extend", data=data)

    def update_segment_users(
        self,
        segment_id: str,
        users: List[str],
        remove: bool = False,
    ) -> Dict[str, Any]:
        """
        Add or remove users from a segment.

        Args:
            segment_id: The segment ID (UUID)
            users: List of user identifiers (emails, IPs, or UUIDs as strings).
                   Maximum 10,000 users per request.
            remove: If True, removes users from the segment. If False (default),
                   adds users to the segment.

        Returns:
            Empty dictionary on success
        """
        data = {
            "users": users,
            "remove": remove,
        }

        return self._make_request("PUT", f"/segment/{segment_id}/users", data=data)
