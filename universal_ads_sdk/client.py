"""
Main client for the Universal Ads SDK.
"""

import json
from typing import Dict, Any, Optional, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import Authenticator
from .exceptions import APIError, AuthenticationError
from .endpoints import (
    CreativeEndpoint,
    MediaEndpoint,
    ReportEndpoint,
    SegmentEndpoint,
)


class UniversalAdsClient:
    """
    Main client for interacting with the Universal Ads API.

    This client provides methods for all available API endpoints including
    creative management, media upload, and reporting.
    """

    BASE_URL = "https://api.universalads.com/v1"

    def __init__(
        self,
        api_key: str,
        private_key_pem: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """
        Initialize the Universal Ads client.

        Args:
            api_key: Your API key
            private_key_pem: Your private key in PEM format
            base_url: Base URL for the API (defaults to production)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout

        # Initialize authenticator
        try:
            self.authenticator = Authenticator(api_key, private_key_pem)
        except Exception as e:
            raise AuthenticationError(f"Failed to initialize authenticator: {e}")

        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Initialize endpoint modules
        self.creative = CreativeEndpoint(self._make_request)
        self.media = MediaEndpoint(self._make_request)
        self.report = ReportEndpoint(self._make_request)
        self.segment = SegmentEndpoint(self._make_request)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the API.

        Args:
            method: HTTP method
            endpoint: API endpoint (without base URL)
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dictionary

        Raises:
            APIError: If the request fails
        """
        # Build URL with query parameters for authentication
        url = f"{self.base_url}{endpoint}"
        if params:
            from urllib.parse import urlencode

            # Ensure list values are encoded as repeated query params (e.g., a=1&a=2)
            query_string = urlencode(params, doseq=True)
            url = f"{url}?{query_string}"

        # Prepare body
        body_str = ""
        if data:
            if isinstance(data, str):
                body_str = data
            else:
                body_str = json.dumps(data)

        # Get authentication headers (using URL with query params)
        headers = self.authenticator.get_auth_headers(method, url, body_str)
        headers["Content-Type"] = "application/json"

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                data=body_str if body_str else None,
                params=None,  # Query params already in URL
                timeout=self.timeout,
            )

            # Handle response
            if response.status_code >= 400:
                error_data = {}
                try:
                    error_data = response.json()
                except:
                    error_data = {"message": response.text}

                raise APIError(
                    message=f"API request failed: {error_data.get('message', 'Unknown error')}",
                    status_code=response.status_code,
                    response_data=error_data,
                )

            # Return JSON response or empty dict for 204
            if response.status_code == 204:
                return {}

            return response.json()

        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    # Creative Management Methods
    # These methods delegate to the creative endpoint for backward compatibility

    def get_creatives(
        self,
        adaccount_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get a list of creatives. Delegates to creative endpoint."""
        return self.creative.get_creatives(
            adaccount_id=adaccount_id, limit=limit, offset=offset, sort=sort
        )

    def get_creative(self, creative_id: str) -> Dict[str, Any]:
        """Get a specific creative by ID. Delegates to creative endpoint."""
        return self.creative.get_creative(creative_id)

    def create_creative(
        self, adaccount_id: str, name: str, media_id: str
    ) -> Dict[str, Any]:
        """Create a new creative. Delegates to creative endpoint."""
        return self.creative.create_creative(adaccount_id, name, media_id)

    def update_creative(
        self, creative_id: str, name: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """Update an existing creative. Delegates to creative endpoint."""
        return self.creative.update_creative(creative_id, name=name, **kwargs)

    def delete_creative(self, creative_id: str) -> Dict[str, Any]:
        """Delete a creative. Delegates to creative endpoint."""
        return self.creative.delete_creative(creative_id)

    # Media Management Methods
    # These methods delegate to the media endpoint for backward compatibility

    def upload_media(
        self, file_path: str, content_type: str, filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload media and get a presigned URL. Delegates to media endpoint."""
        return self.media.upload_media(file_path, content_type, filename)

    def verify_media(self, media_id: str) -> Dict[str, Any]:
        """Verify that a media upload is complete. Delegates to media endpoint."""
        return self.media.verify_media(media_id)

    # Reporting Methods
    # These methods delegate to the report endpoint for backward compatibility

    def get_campaign_report(
        self,
        start_date: str,
        end_date: str,
        adaccount_id: Optional[str] = None,
        campaign_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get campaign performance report. Delegates to report endpoint."""
        return self.report.get_campaign_report(
            start_date=start_date,
            end_date=end_date,
            adaccount_id=adaccount_id,
            campaign_ids=campaign_ids,
            limit=limit,
            offset=offset,
        )

    def get_adset_report(
        self,
        start_date: str,
        end_date: str,
        adaccount_id: Optional[str] = None,
        adset_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get adset performance report. Delegates to report endpoint."""
        return self.report.get_adset_report(
            start_date=start_date,
            end_date=end_date,
            adaccount_id=adaccount_id,
            adset_ids=adset_ids,
            limit=limit,
            offset=offset,
        )

    def get_ad_report(
        self,
        start_date: str,
        end_date: str,
        adaccount_id: Optional[str] = None,
        ad_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get ad performance report. Delegates to report endpoint."""
        return self.report.get_ad_report(
            start_date=start_date,
            end_date=end_date,
            adaccount_id=adaccount_id,
            ad_ids=ad_ids,
            limit=limit,
            offset=offset,
        )

    # Segment Management Methods
    # These methods delegate to the segment endpoint for backward compatibility

    def create_segment(
        self,
        adaccount_id: str,
        media_id: str,
        name: str,
        segment_type: str,
        description: Optional[str] = None,
        large_files: bool = False,
    ) -> Dict[str, Any]:
        """Create a new custom segment. Delegates to segment endpoint."""
        return self.segment.create_segment(
            adaccount_id=adaccount_id,
            media_id=media_id,
            name=name,
            segment_type=segment_type,
            description=description,
            large_files=large_files,
        )

    def get_segments(
        self,
        adaccount_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        segment_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get a list of custom segments. Delegates to segment endpoint."""
        return self.segment.get_segments(
            adaccount_id=adaccount_id,
            name=name,
            description=description,
            status=status,
            segment_ids=segment_ids,
            limit=limit,
            offset=offset,
            sort=sort,
        )

    def get_segment(self, segment_id: str) -> Dict[str, Any]:
        """Get a specific segment by ID. Delegates to segment endpoint."""
        return self.segment.get_segment(segment_id)

    def update_segment(
        self,
        segment_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an existing segment. Delegates to segment endpoint."""
        return self.segment.update_segment(
            segment_id=segment_id, name=name, description=description
        )

    def delete_segment(self, segment_id: str) -> Dict[str, Any]:
        """Delete a segment. Delegates to segment endpoint."""
        return self.segment.delete_segment(segment_id)

    def extend_segment(
        self,
        segment_id: str,
        media_id: str,
        large_files: bool = False,
    ) -> Dict[str, Any]:
        """Extend a segment with additional media. Delegates to segment endpoint."""
        return self.segment.extend_segment(
            segment_id=segment_id, media_id=media_id, large_files=large_files
        )

    def update_segment_users(
        self,
        segment_id: str,
        users: list,
        remove: bool = False,
    ) -> Dict[str, Any]:
        """Add or remove users from a segment. Delegates to segment endpoint."""
        return self.segment.update_segment_users(
            segment_id=segment_id, users=users, remove=remove
        )
