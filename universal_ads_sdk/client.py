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

            query_string = urlencode(params)
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
        data = {"adaccount_id": adaccount_id, "name": name, "media_id": media_id}
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

    # Media Management Methods

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
        import os

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

    # Reporting Methods

    def get_campaign_report(
        self,
        start_date: str,
        end_date: str,
        adaccount_id: Optional[str] = None,
        campaign_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get campaign performance report.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            adaccount_id: Filter by ad account ID
            campaign_ids: List of campaign IDs to include
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Dictionary containing campaign report data
        """
        params = {"start_date": start_date, "end_date": end_date}

        if adaccount_id:
            params["adaccount_id"] = adaccount_id
        if campaign_ids:
            params["campaign_ids"] = campaign_ids
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/report/campaign", params=params)

    def get_adset_report(
        self,
        start_date: str,
        end_date: str,
        adaccount_id: Optional[str] = None,
        adset_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get adset performance report.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            adaccount_id: Filter by ad account ID
            adset_ids: List of adset IDs to include
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Dictionary containing adset report data
        """
        params = {"start_date": start_date, "end_date": end_date}

        if adaccount_id:
            params["adaccount_id"] = adaccount_id
        if adset_ids:
            params["adset_ids"] = adset_ids
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/report/adset", params=params)

    def get_ad_report(
        self,
        start_date: str,
        end_date: str,
        adaccount_id: Optional[str] = None,
        ad_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get ad performance report.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            adaccount_id: Filter by ad account ID
            ad_ids: List of ad IDs to include
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Dictionary containing ad report data
        """
        params = {"start_date": start_date, "end_date": end_date}

        if adaccount_id:
            params["adaccount_id"] = adaccount_id
        if ad_ids:
            params["ad_ids"] = ad_ids
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/report/ad", params=params)
