"""
Media management endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class MediaEndpoint(BaseEndpoint):
    """Endpoint for managing media uploads."""

    def upload_media(
        self,
        mime_type: str,
        adaccount_id: Optional[str],
        name: Optional[str],
    ) -> Dict[str, Any]:
        """
        Generate a presigned URL for file upload.

        Args:
            mime_type: MIME type of the file
            adaccount_id: Ad account ID (UUID, can be None)
            name: Name of the media file (can be None)

        Returns:
            Dictionary containing upload information including presigned URL
        """
        data = {
            "mime_type": mime_type,
            "adaccount_id": adaccount_id,
            "name": name,
        }

        return self._make_request("POST", "/media", data=data)

    def get_media(self, media_id: str) -> Dict[str, Any]:
        """
        Retrieve information on a specific media.

        Args:
            media_id: Unique ID of the media to be retrieved (UUID)

        Returns:
            Dictionary containing media information
        """
        return self._make_request("GET", f"/media/{media_id}")

    def verify_media(self, media_id: str) -> Dict[str, Any]:
        """
        Verify that a media upload is complete and valid.

        Args:
            media_id: The media ID to verify

        Returns:
            Dictionary containing media verification status
        """
        return self._make_request("POST", f"/media/{media_id}/verify")
