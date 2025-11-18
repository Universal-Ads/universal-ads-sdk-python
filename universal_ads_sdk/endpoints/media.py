"""
Media management endpoints.
"""

import os
from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class MediaEndpoint(BaseEndpoint):
    """Endpoint for managing media uploads."""

    def upload_media(
        self, file_path: str, content_type: str, filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload media and get a presigned URL for file upload.

        Args:
            file_path: Path to the file to upload
            content_type: MIME type of the file
            filename: Optional filename (defaults to basename of file_path)

        Returns:
            Dictionary containing upload information including presigned URL
        """
        if not filename:
            filename = os.path.basename(file_path)

        data = {"filename": filename, "content_type": content_type}

        return self._make_request("POST", "/media", data=data)

    def verify_media(self, media_id: str) -> Dict[str, Any]:
        """
        Verify that a media upload is complete and valid.

        Args:
            media_id: The media ID to verify

        Returns:
            Dictionary containing media verification status
        """
        return self._make_request("POST", f"/media/{media_id}/verify")
