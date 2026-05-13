"""
Pixel endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class PixelEndpoint(BaseEndpoint):
    """Endpoint for accessing enhanced pixels."""

    def get_pixels(
        self,
        adaccount_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get a list of pixels."""
        params: Dict[str, Any] = {"adaccount_id": adaccount_id}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        return self._make_request("GET", "/pixels", params=params)

    def get_pixel(self, pixel_id: str) -> Dict[str, Any]:
        """Get a specific pixel by ID."""
        return self._make_request("GET", f"/pixels/{pixel_id}")

    def get_pixel_events(
        self,
        pixel_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get events associated with a pixel."""
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        params.update(kwargs)

        return self._make_request("GET", f"/pixels/{pixel_id}/events", params=params)
