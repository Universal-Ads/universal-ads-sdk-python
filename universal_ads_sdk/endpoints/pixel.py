"""
Pixel endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class PixelEndpoint(BaseEndpoint):
    """Endpoint for accessing enhanced pixels."""

    def get_pixels(
        self,
        adaccount_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of pixels."""
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
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        params.update(kwargs)

        return self._make_request("GET", f"/pixels/{pixel_id}/events", params=params)
