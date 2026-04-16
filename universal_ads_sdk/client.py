"""
Main client for the Universal Ads SDK.
"""

import json
from typing import Dict, Any, Optional, Union, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import Authenticator
from .common.exceptions import APIError, AuthenticationError
from .endpoints import (
    CreativeEndpoint,
    MediaEndpoint,
    ReportEndpoint,
    SegmentEndpoint,
    MeEndpoint,
    CampaignEndpoint,
    AdsetEndpoint,
    AdEndpoint,
    PixelEndpoint,
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
        self.me = MeEndpoint(self._make_request)
        self.campaign = CampaignEndpoint(self._make_request)
        self.adset = AdsetEndpoint(self._make_request)
        self.ad = AdEndpoint(self._make_request)
        self.pixel = PixelEndpoint(self._make_request)

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
        campaign_id: Optional[str] = None,
        adset_id: Optional[str] = None,
        ad_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get a list of creatives. Delegates to creative endpoint."""
        return self.creative.get_creatives(
            adaccount_id=adaccount_id,
            campaign_id=campaign_id,
            adset_id=adset_id,
            ad_id=ad_id,
            limit=limit,
            offset=offset,
            sort=sort,
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
        self,
        file_path: Optional[str] = None,
        content_type: Optional[str] = None,
        filename: Optional[str] = None,
        mime_type: Optional[str] = None,
        adaccount_id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload media and get a presigned URL. Delegates to media endpoint.

        For backward compatibility, accepts file_path/content_type/filename.
        New API format uses mime_type/adaccount_id/name.

        Args:
            file_path: Path to file (for backward compatibility, used to extract name)
            content_type: MIME type (for backward compatibility, maps to mime_type)
            filename: Filename (for backward compatibility, maps to name)
            mime_type: MIME type of the file (new API format)
            adaccount_id: Ad account ID (UUID, can be None)
            name: Name of the media file (can be None)
        """
        # Backward compatibility: convert old format to new format
        if file_path is not None or content_type is not None:
            import os

            final_mime_type = mime_type or content_type
            final_name = (
                name or filename or (os.path.basename(file_path) if file_path else None)
            )
            return self.media.upload_media(
                mime_type=final_mime_type,
                adaccount_id=adaccount_id,
                name=final_name,
            )
        # New API format
        return self.media.upload_media(
            mime_type=mime_type,
            adaccount_id=adaccount_id,
            name=name,
        )

    def get_media(self, media_id: str) -> Dict[str, Any]:
        """Get information on a specific media. Delegates to media endpoint."""
        return self.media.get_media(media_id)

    def verify_media(self, media_id: str) -> Dict[str, Any]:
        """Verify that a media upload is complete. Delegates to media endpoint."""
        return self.media.verify_media(media_id)

    # Reporting Methods
    # These methods delegate to the report endpoint for backward compatibility

    def get_campaign_report(
        self,
        adaccount_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        campaign_ids: Optional[list] = None,
        adset_ids: Optional[list] = None,
        ad_ids: Optional[list] = None,
        date_aggregation: Optional[Union[str, "ReportTimeAggregation"]] = None,
        attribution_window: Optional[Union[str, "AttributionWindowEnum"]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get campaign performance report. Delegates to report endpoint."""
        return self.report.get_campaign_report(
            adaccount_id=adaccount_id,
            start_date=start_date,
            end_date=end_date,
            campaign_ids=campaign_ids,
            adset_ids=adset_ids,
            ad_ids=ad_ids,
            date_aggregation=date_aggregation,
            attribution_window=attribution_window,
            limit=limit,
            offset=offset,
        )

    def get_adset_report(
        self,
        adaccount_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        campaign_ids: Optional[list] = None,
        adset_ids: Optional[list] = None,
        ad_ids: Optional[list] = None,
        date_aggregation: Optional[Union[str, "ReportTimeAggregation"]] = None,
        attribution_window: Optional[Union[str, "AttributionWindowEnum"]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get adset performance report. Delegates to report endpoint."""
        return self.report.get_adset_report(
            adaccount_id=adaccount_id,
            start_date=start_date,
            end_date=end_date,
            campaign_ids=campaign_ids,
            adset_ids=adset_ids,
            ad_ids=ad_ids,
            date_aggregation=date_aggregation,
            attribution_window=attribution_window,
            limit=limit,
            offset=offset,
        )

    def get_ad_report(
        self,
        adaccount_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        campaign_ids: Optional[list] = None,
        adset_ids: Optional[list] = None,
        ad_ids: Optional[list] = None,
        date_aggregation: Optional[Union[str, "ReportTimeAggregation"]] = None,
        attribution_window: Optional[Union[str, "AttributionWindowEnum"]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get ad performance report. Delegates to report endpoint."""
        return self.report.get_ad_report(
            adaccount_id=adaccount_id,
            start_date=start_date,
            end_date=end_date,
            campaign_ids=campaign_ids,
            adset_ids=adset_ids,
            ad_ids=ad_ids,
            date_aggregation=date_aggregation,
            attribution_window=attribution_window,
            limit=limit,
            offset=offset,
        )

    def schedule_report(
        self,
        start_date: str,
        end_date: str,
        entity_level: Union[str, "EntityLevel"],
        adaccount_ids: list,
        campaign_ids: Optional[list] = None,
        adset_ids: Optional[list] = None,
        ad_ids: Optional[list] = None,
        dimensions: Optional[list] = None,
        time_aggregation: Optional[Union[str, "TimeAggregation"]] = None,
        attribution_window: Optional[Union[str, "AttributionWindowEnum"]] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Schedule a report for asynchronous processing. Delegates to report endpoint."""
        return self.report.schedule_report(
            start_date=start_date,
            end_date=end_date,
            entity_level=entity_level,
            adaccount_ids=adaccount_ids,
            campaign_ids=campaign_ids,
            adset_ids=adset_ids,
            ad_ids=ad_ids,
            dimensions=dimensions,
            time_aggregation=time_aggregation,
            attribution_window=attribution_window,
            limit=limit,
        )

    def get_scheduled_report(self, scheduled_report_id: str) -> Dict[str, Any]:
        """Get information about a scheduled report. Delegates to report endpoint."""
        return self.report.get_scheduled_report(scheduled_report_id)

    # Segment Management Methods
    # These methods delegate to the segment endpoint for backward compatibility

    def create_segment(
        self,
        adaccount_id: str,
        name: str,
        segment_type: str,
        media_id: Optional[str] = None,
        users: Optional[list] = None,
        description: Optional[str] = None,
        large_files: bool = False,
    ) -> Dict[str, Any]:
        """Create a new custom segment. Delegates to segment endpoint."""
        return self.segment.create_segment(
            adaccount_id=adaccount_id,
            name=name,
            segment_type=segment_type,
            media_id=media_id,
            users=users,
            description=description,
            large_files=large_files,
        )

    def get_segments(
        self,
        adaccount_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        audience_ids: Optional[list] = None,
        segment_ids: Optional[list] = None,
        segment_type: Optional[str] = None,
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
            audience_ids=audience_ids,
            segment_ids=segment_ids,
            segment_type=segment_type,
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

    # Me Endpoints
    # These methods delegate to the me endpoint

    def get_organizations(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get all organizations that the authenticated application has organization-level scopes for. Delegates to me endpoint."""
        return self.me.get_organizations(limit=limit, offset=offset)

    def get_adaccounts(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        organization_ids: Optional[List[str]] = None,
        authorization_statuses: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Get all ad accounts that the authenticated application has ad account-level or organization-level scopes for. Delegates to me endpoint."""
        return self.me.get_adaccounts(
            limit=limit,
            offset=offset,
            organization_ids=organization_ids,
            authorization_statuses=authorization_statuses,
        )

    # Campaign Management Methods
    # These methods delegate to the campaign endpoint

    def get_campaigns(
        self,
        adaccount_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of campaigns. Delegates to campaign endpoint."""
        return self.campaign.get_campaigns(
            adaccount_id=adaccount_id,
            limit=limit,
            offset=offset,
            sort=sort,
            **kwargs,
        )

    def get_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Get a specific campaign by ID. Delegates to campaign endpoint."""
        return self.campaign.get_campaign(campaign_id)

    def create_campaign(self, **data) -> Dict[str, Any]:
        """Create a campaign. Delegates to campaign endpoint."""
        return self.campaign.create_campaign(**data)

    def update_campaign(self, campaign_id: str, **data) -> Dict[str, Any]:
        """Update a campaign. Delegates to campaign endpoint."""
        return self.campaign.update_campaign(campaign_id, **data)

    # Ad Set Management Methods
    # These methods delegate to the adset endpoint

    def get_adsets(
        self,
        adaccount_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of ad sets. Delegates to adset endpoint."""
        return self.adset.get_adsets(
            adaccount_id=adaccount_id,
            campaign_id=campaign_id,
            limit=limit,
            offset=offset,
            sort=sort,
            **kwargs,
        )

    def get_adset(self, adset_id: str) -> Dict[str, Any]:
        """Get a specific ad set by ID. Delegates to adset endpoint."""
        return self.adset.get_adset(adset_id)

    def create_adset(self, **data) -> Dict[str, Any]:
        """Create an ad set. Delegates to adset endpoint."""
        return self.adset.create_adset(**data)

    def update_adset(self, adset_id: str, **data) -> Dict[str, Any]:
        """Update an ad set. Delegates to adset endpoint."""
        return self.adset.update_adset(adset_id, **data)

    # Ad Management Methods
    # These methods delegate to the ad endpoint

    def get_ads(
        self,
        adaccount_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        adset_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of ads. Delegates to ad endpoint."""
        return self.ad.get_ads(
            adaccount_id=adaccount_id,
            campaign_id=campaign_id,
            adset_id=adset_id,
            limit=limit,
            offset=offset,
            sort=sort,
            **kwargs,
        )

    def get_ad(self, ad_id: str) -> Dict[str, Any]:
        """Get a specific ad by ID. Delegates to ad endpoint."""
        return self.ad.get_ad(ad_id)

    def create_ad(self, **data) -> Dict[str, Any]:
        """Create an ad. Delegates to ad endpoint."""
        return self.ad.create_ad(**data)

    def update_ad(self, ad_id: str, **data) -> Dict[str, Any]:
        """Update an ad. Delegates to ad endpoint."""
        return self.ad.update_ad(ad_id, **data)

    # Pixel Methods
    # These methods delegate to the pixel endpoint

    def get_pixels(
        self,
        adaccount_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of pixels. Delegates to pixel endpoint."""
        return self.pixel.get_pixels(
            adaccount_id=adaccount_id,
            limit=limit,
            offset=offset,
            sort=sort,
            **kwargs,
        )

    def get_pixel(self, pixel_id: str) -> Dict[str, Any]:
        """Get a specific pixel by ID. Delegates to pixel endpoint."""
        return self.pixel.get_pixel(pixel_id)

    def get_pixel_events(
        self,
        pixel_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get pixel events. Delegates to pixel endpoint."""
        return self.pixel.get_pixel_events(
            pixel_id=pixel_id,
            limit=limit,
            offset=offset,
            **kwargs,
        )
