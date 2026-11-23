"""
Main client for the Universal Ads SDK.
"""

import json
import random
import time
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Union, cast

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import Authenticator, sdk_identity_headers
from .common.exceptions import (
    APIError,
    ArchiveJobTimeoutError,
    AuthenticationError,
    TokenError,
    TokenStoreError,
)
from .common.types import ArchiveJobStatus
from .endpoints import (
    AdEndpoint,
    AdsetEndpoint,
    ArchiveJobEndpoint,
    AudienceEndpoint,
    CampaignEndpoint,
    CreativeEndpoint,
    MediaEndpoint,
    MeEndpoint,
    PixelEndpoint,
    ReportEndpoint,
)


class _PendingTokenStore(NamedTuple):
    access_token: str
    expires_at: float
    refresh_token: str
    scope: Optional[str]


class _ParsedToken(NamedTuple):
    access_token: str
    expires_in: float
    refresh_token: Optional[str]
    scope: Optional[str]


class _OAuthErrorBody(NamedTuple):
    error: Optional[str]
    error_description: Optional[str]


def _require_text(name: str, value: object) -> str:
    if not isinstance(value, str) or value == "":
        raise ValueError(f"{name} must be a non-empty string.")
    return value


def _require_expiry(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("access_token_expires_at must be a Unix timestamp in seconds.")
    return float(value)


class UniversalAdsClient:
    """
    Main client for interacting with the Universal Ads API.

    This client provides methods for all available API endpoints including
    creative management, media upload, and reporting.
    """

    BASE_URL = "https://api.universalads.com/v1"
    _RESERVED_AUTH_HEADERS = {"x-api-key", "x-timestamp", "x-signature"}

    def __init__(
        self,
        api_key: Optional[str] = None,
        private_key_pem: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        headers: Optional[Dict[str, str]] = None,
        *,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        refresh_token: Optional[str] = None,
        access_token: Optional[str] = None,
        access_token_expires_at: Optional[float] = None,
        store_hook: Optional[Callable[..., None]] = None,
        system_user_id: Optional[str] = None,
    ):
        """
        Initialize the Universal Ads client.

        A signed client takes api_key and private_key_pem. A token client takes
        one of: client_id, client_secret, refresh_token, and store_hook;
        client_id, client_secret, and system_user_id; or access_token alone.
        """
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self._configure_credentials(
            api_key=api_key,
            private_key_pem=private_key_pem,
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            access_token=access_token,
            access_token_expires_at=access_token_expires_at,
            store_hook=store_hook,
            system_user_id=system_user_id,
        )
        self._custom_headers = self._sanitize_custom_headers(headers)

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
        self.audience = AudienceEndpoint(self._make_request)
        self.me = MeEndpoint(self._make_request)
        self.campaign = CampaignEndpoint(self._make_request)
        self.adset = AdsetEndpoint(self._make_request)
        self.ad = AdEndpoint(self._make_request)
        self.pixel = PixelEndpoint(self._make_request)
        self.archive_job = ArchiveJobEndpoint(self._make_request)

    def __repr__(self) -> str:
        return (
            f"UniversalAdsClient(base_url={self.base_url!r}, "
            f"credential={self._credential!r})"
        )

    def _configure_credentials(
        self,
        *,
        api_key: Optional[str],
        private_key_pem: Optional[str],
        client_id: Optional[str],
        client_secret: Optional[str],
        refresh_token: Optional[str],
        access_token: Optional[str],
        access_token_expires_at: Optional[float],
        store_hook: Optional[Callable[..., None]],
        system_user_id: Optional[str],
    ) -> None:
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.access_token_expires_at: Optional[float] = None
        self.scope: Optional[str] = None
        self.authenticator: Optional[Authenticator] = None
        self._client_id: Optional[str] = None
        self._client_secret: Optional[str] = None
        self._store_hook: Optional[Callable[..., None]] = None
        self._system_user_id: Optional[str] = None
        self._pending_store: Optional[_PendingTokenStore] = None

        signing = api_key is not None or private_key_pem is not None
        oauth = any(
            value is not None
            for value in (
                client_id,
                client_secret,
                refresh_token,
                access_token,
                access_token_expires_at,
                store_hook,
                system_user_id,
            )
        )
        if signing and oauth:
            raise ValueError("Signing keys and OAuth credentials cannot be combined.")
        if not signing and not oauth:
            raise ValueError(
                "Provide an API key and private key, or OAuth credentials."
            )
        if signing:
            self._configure_signed_client(api_key, private_key_pem)
            return
        if system_user_id is not None:
            self._configure_system_user_client(
                client_id=client_id,
                client_secret=client_secret,
                refresh_token=refresh_token,
                access_token=access_token,
                access_token_expires_at=access_token_expires_at,
                store_hook=store_hook,
                system_user_id=system_user_id,
            )
            return
        if any(
            value is not None
            for value in (client_id, client_secret, refresh_token, store_hook)
        ):
            self._configure_refresh_client(
                client_id=client_id,
                client_secret=client_secret,
                refresh_token=refresh_token,
                access_token=access_token,
                access_token_expires_at=access_token_expires_at,
                store_hook=store_hook,
            )
            return
        self._configure_access_token_client(access_token, access_token_expires_at)

    def _configure_signed_client(
        self, api_key: Optional[str], private_key_pem: Optional[str]
    ) -> None:
        if api_key is None or private_key_pem is None:
            raise ValueError(
                "api_key and private_key_pem are both required to sign requests."
            )
        api_key = _require_text("api_key", api_key)
        private_key_pem = _require_text("private_key_pem", private_key_pem)
        self._credential = "signed"
        try:
            self.authenticator = Authenticator(api_key, private_key_pem)
        except Exception as e:
            raise AuthenticationError(f"Failed to initialize authenticator: {e}")

    def _configure_refresh_client(
        self,
        *,
        client_id: Optional[str],
        client_secret: Optional[str],
        refresh_token: Optional[str],
        access_token: Optional[str],
        access_token_expires_at: Optional[float],
        store_hook: Optional[Callable[..., None]],
    ) -> None:
        if (
            client_id is None
            or client_secret is None
            or refresh_token is None
            or store_hook is None
        ):
            raise ValueError(
                "A refresh-token client requires client_id, client_secret, "
                "refresh_token, and store_hook."
            )
        if not callable(store_hook):
            raise ValueError("store_hook must be callable.")
        has_access_token = access_token is not None
        has_expiry = access_token_expires_at is not None
        if has_access_token != has_expiry:
            raise ValueError(
                "access_token and access_token_expires_at must be provided together."
            )
        self._credential = "refresh_token"
        self._client_id = _require_text("client_id", client_id)
        self._client_secret = _require_text("client_secret", client_secret)
        self.refresh_token = _require_text("refresh_token", refresh_token)
        self._store_hook = store_hook
        if has_access_token:
            self.access_token = _require_text("access_token", access_token)
            self.access_token_expires_at = _require_expiry(access_token_expires_at)

    def _configure_system_user_client(
        self,
        *,
        client_id: Optional[str],
        client_secret: Optional[str],
        refresh_token: Optional[str],
        access_token: Optional[str],
        access_token_expires_at: Optional[float],
        store_hook: Optional[Callable[..., None]],
        system_user_id: str,
    ) -> None:
        if any(
            value is not None
            for value in (
                refresh_token,
                access_token,
                access_token_expires_at,
                store_hook,
            )
        ):
            raise ValueError(
                "A system-user client takes client_id, client_secret, and "
                "system_user_id."
            )
        if client_id is None or client_secret is None:
            raise ValueError(
                "A system-user client requires client_id, client_secret, and "
                "system_user_id."
            )
        self._credential = "system_user"
        self._client_id = _require_text("client_id", client_id)
        self._client_secret = _require_text("client_secret", client_secret)
        self._system_user_id = _require_text("system_user_id", system_user_id)

    def _configure_access_token_client(
        self,
        access_token: Optional[str],
        access_token_expires_at: Optional[float],
    ) -> None:
        if access_token_expires_at is not None or access_token is None:
            raise ValueError("An access-token client takes an access token alone.")
        self._credential = "access_token"
        self.access_token = _require_text("access_token", access_token)

    def _sanitize_custom_headers(
        self, headers: Optional[Dict[str, str]]
    ) -> Dict[str, str]:
        """Validate and normalize user-provided custom headers."""
        if not headers:
            return {}

        reserved = set(self._RESERVED_AUTH_HEADERS)
        if self._credential != "signed":
            reserved.add("authorization")

        sanitized_headers: Dict[str, str] = {}
        for key, value in headers.items():
            if key.lower() in reserved:
                raise ValueError(
                    f"Custom header '{key}' cannot override SDK authentication headers."
                )
            sanitized_headers[key] = str(value)

        return sanitized_headers

    def _ensure_access_token(self) -> None:
        expires_at = self.access_token_expires_at
        if self._credential == "access_token":
            return
        if self._pending_store is not None:
            self._run_store_hook(self._pending_store)
            return
        if (
            self.access_token is not None
            and expires_at is not None
            and expires_at - time.time() > 60
        ):
            return
        self._request_access_token()

    def _request_access_token(self) -> None:
        if self._credential == "refresh_token":
            form = {
                "grant_type": "refresh_token",
                "refresh_token": cast(str, self.refresh_token),
            }
        else:
            form = {
                "grant_type": "client_credentials",
                "system_user_id": cast(str, self._system_user_id),
            }
        try:
            response = requests.post(
                url=f"{self.base_url.rstrip('/')}/oauth/token",
                data=form,
                auth=(cast(str, self._client_id), cast(str, self._client_secret)),
                allow_redirects=False,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise TokenError("Token request failed") from exc

        if not 200 <= response.status_code < 300:
            raise self._token_error(response)

        parsed = self._read_token_body(response)
        expires_at = time.time() + parsed.expires_in
        self.access_token = parsed.access_token
        self.access_token_expires_at = expires_at
        self.scope = parsed.scope
        if parsed.refresh_token is None:
            return
        self.refresh_token = parsed.refresh_token
        pending = _PendingTokenStore(
            access_token=parsed.access_token,
            expires_at=expires_at,
            refresh_token=parsed.refresh_token,
            scope=parsed.scope,
        )
        self._pending_store = pending
        self._run_store_hook(pending)

    def _read_token_body(self, response: requests.Response) -> _ParsedToken:
        try:
            body = response.json()
        except ValueError:
            body = None
        if not isinstance(body, dict):
            raise self._unreadable_token_error(response)

        access_token = body.get("access_token")
        expires_in = body.get("expires_in")
        if not isinstance(access_token, str) or access_token == "":
            raise self._unreadable_token_error(response)
        if isinstance(expires_in, bool) or not isinstance(expires_in, (int, float)):
            raise self._unreadable_token_error(response)

        scope = body.get("scope")
        if scope is not None and not isinstance(scope, str):
            raise self._unreadable_token_error(response)

        refresh_token: Optional[str] = None
        if self._credential == "refresh_token":
            refresh_value = body.get("refresh_token")
            if not isinstance(refresh_value, str) or refresh_value == "":
                raise self._unreadable_token_error(response)
            refresh_token = refresh_value
        return _ParsedToken(access_token, float(expires_in), refresh_token, scope)

    def _token_error(self, response: requests.Response) -> TokenError:
        fields = self._token_error_fields(response)
        message = f"HTTP {response.status_code}"
        if fields.error is not None:
            message = f"{message}: {fields.error}"
        if fields.error_description is not None:
            message = f"{message}: {fields.error_description}"
        return TokenError(
            message,
            status_code=response.status_code,
            error=fields.error,
            error_description=fields.error_description,
        )

    def _token_error_fields(self, response: requests.Response) -> _OAuthErrorBody:
        try:
            body = response.json()
        except ValueError:
            return _OAuthErrorBody(None, None)
        if not isinstance(body, dict):
            return _OAuthErrorBody(None, None)
        error = body.get("error")
        error_description = body.get("error_description")
        if not isinstance(error, str):
            error = None
        if not isinstance(error_description, str):
            error_description = None
        return _OAuthErrorBody(error, error_description)

    def _unreadable_token_error(self, response: requests.Response) -> TokenError:
        return TokenError(
            f"HTTP {response.status_code}: unreadable token response",
            status_code=response.status_code,
        )

    def _run_store_hook(self, pending: _PendingTokenStore) -> None:
        try:
            cast(Callable[..., None], self._store_hook)(
                access_token=pending.access_token,
                expires_at=pending.expires_at,
                refresh_token=pending.refresh_token,
                scope=pending.scope,
            )
        except Exception as exc:
            raise TokenStoreError("Token store hook failed") from exc
        self._pending_store = None

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
            APIError: If the API request fails
            TokenError: If a token request fails before the API call
            TokenStoreError: If the store hook fails before the API call
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
        authenticator = self.authenticator
        if authenticator is not None:
            headers = authenticator.get_auth_headers(method, url, body_str)
        else:
            self._ensure_access_token()
            headers = {"Authorization": f"Bearer {cast(str, self.access_token)}"}
            headers.update(sdk_identity_headers())
        if self._custom_headers:
            headers.update(self._custom_headers)
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

    # Audience Management Methods
    # These methods delegate to the audience endpoint

    def create_audience(
        self,
        adaccount_id: str,
        name: str,
        segment_type: str,
        media_id: Optional[str] = None,
        users: Optional[list] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new custom audience. Delegates to audience endpoint."""
        return self.audience.create_audience(
            adaccount_id=adaccount_id,
            name=name,
            segment_type=segment_type,
            media_id=media_id,
            users=users,
            description=description,
        )

    def get_audiences(
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
        """Get a list of custom audiences. Delegates to audience endpoint."""
        return self.audience.get_audiences(
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

    def get_audience(self, audience_id: str) -> Dict[str, Any]:
        """Get a specific audience by ID. Delegates to audience endpoint."""
        return self.audience.get_audience(audience_id)

    def update_audience(
        self,
        audience_id: str,
        name: str,
        description: str,
    ) -> Dict[str, Any]:
        """Update an existing audience. Delegates to audience endpoint."""
        return self.audience.update_audience(
            audience_id=audience_id, name=name, description=description
        )

    def delete_audience(self, audience_id: str) -> Dict[str, Any]:
        """Delete an audience. Delegates to audience endpoint."""
        return self.audience.delete_audience(audience_id)

    def update_audience_users(
        self,
        audience_id: str,
        users: Optional[list] = None,
        media_id: Optional[str] = None,
        remove: bool = False,
    ) -> Dict[str, Any]:
        """Add or remove users from an audience. Delegates to audience endpoint."""
        return self.audience.update_audience_users(
            audience_id=audience_id,
            users=users,
            media_id=media_id,
            remove=remove,
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
        adaccount_id: str,
        campaign_ids: Optional[list] = None,
        name: Optional[str] = None,
        status: Optional[Union[str, List[str]]] = None,
        campaign_type: Optional[str] = None,
        include_archived: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of campaigns. Delegates to campaign endpoint."""
        return self.campaign.get_campaigns(
            adaccount_id=adaccount_id,
            campaign_ids=campaign_ids,
            name=name,
            status=status,
            campaign_type=campaign_type,
            include_archived=include_archived,
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
        adaccount_id: str,
        campaign_ids: Optional[list] = None,
        adset_ids: Optional[list] = None,
        name: Optional[str] = None,
        status: Optional[list] = None,
        include_archived: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of ad sets. Delegates to adset endpoint."""
        return self.adset.get_adsets(
            adaccount_id=adaccount_id,
            campaign_ids=campaign_ids,
            adset_ids=adset_ids,
            name=name,
            status=status,
            include_archived=include_archived,
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
        adaccount_id: str,
        campaign_ids: Optional[list] = None,
        adset_ids: Optional[list] = None,
        ad_ids: Optional[list] = None,
        status: Optional[list] = None,
        include_archived: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get a list of ads. Delegates to ad endpoint."""
        return self.ad.get_ads(
            adaccount_id=adaccount_id,
            campaign_ids=campaign_ids,
            adset_ids=adset_ids,
            ad_ids=ad_ids,
            status=status,
            include_archived=include_archived,
            limit=limit,
            offset=offset,
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

    def archive_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Start async campaign archive. Delegates to campaign endpoint."""
        return self.campaign.archive_campaign(campaign_id)

    def unarchive_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Start async campaign unarchive. Delegates to campaign endpoint."""
        return self.campaign.unarchive_campaign(campaign_id)

    def archive_adset(self, adset_id: str) -> Dict[str, Any]:
        """Start async ad set archive. Delegates to adset endpoint."""
        return self.adset.archive_adset(adset_id)

    def unarchive_adset(self, adset_id: str) -> Dict[str, Any]:
        """Start async ad set unarchive. Delegates to adset endpoint."""
        return self.adset.unarchive_adset(adset_id)

    def archive_ad(self, ad_id: str) -> Dict[str, Any]:
        """Start async ad archive. Delegates to ad endpoint."""
        return self.ad.archive_ad(ad_id)

    def unarchive_ad(self, ad_id: str) -> Dict[str, Any]:
        """Start async ad unarchive. Delegates to ad endpoint."""
        return self.ad.unarchive_ad(ad_id)

    def get_archive_job(self, archive_job_id: str) -> Dict[str, Any]:
        """Poll archive job status. Delegates to archive_job endpoint."""
        return self.archive_job.get_archive_job(archive_job_id)

    def poll_archive_job(
        self,
        archive_job_id: str,
        polling_timeout_seconds: Optional[int] = None,
        *,
        archive_start_response: Optional[Dict[str, Any]] = None,
        initial_backoff_seconds: float = 0.5,
        max_backoff_seconds: float = 5.0,
    ) -> Dict[str, Any]:
        """
        Poll GET /archive-job/{id} until status is terminal or timeout.

        Terminal statuses: completed, partially_failed, failed.

        Provide ``polling_timeout_seconds`` or pass ``archive_start_response``
        from the archive/unarchive POST so ``polling_timeout_seconds`` can be
        read from the API. On ``completed``, strict success may still require
        ``failed_entities`` to be empty.

        Raises:
            ArchiveJobTimeoutError: If elapsed time exceeds the timeout.
            ValueError: If timeout cannot be resolved or job id mismatches start response.
        """
        resolved_timeout = polling_timeout_seconds
        if resolved_timeout is None and archive_start_response is not None:
            resolved_timeout = archive_start_response.get("polling_timeout_seconds")
        if resolved_timeout is None:
            raise ValueError(
                "polling_timeout_seconds is required unless archive_start_response "
                "includes polling_timeout_seconds"
            )

        if archive_start_response is not None:
            start_job_id = archive_start_response.get("archive_job_id")
            if start_job_id is not None and start_job_id != archive_job_id:
                raise ValueError(
                    "archive_job_id does not match archive_start_response['archive_job_id']"
                )

        terminal = {
            ArchiveJobStatus.COMPLETED.value,
            ArchiveJobStatus.PARTIALLY_FAILED.value,
            ArchiveJobStatus.FAILED.value,
        }
        start = time.monotonic()
        last_state: Dict[str, Any] = {}
        last_error: Optional[APIError] = None
        backoff = initial_backoff_seconds

        while True:
            elapsed = time.monotonic() - start
            if elapsed >= resolved_timeout:
                raise ArchiveJobTimeoutError(
                    f"Archive job {archive_job_id} polling exceeded "
                    f"{resolved_timeout}s timeout",
                    archive_job_id=archive_job_id,
                    last_job_state=last_state,
                    last_api_error=last_error,
                )

            try:
                last_state = self.get_archive_job(archive_job_id)
                last_error = None
            except APIError as e:
                last_error = e
                remaining = resolved_timeout - (time.monotonic() - start)
                if remaining <= 0:
                    raise ArchiveJobTimeoutError(
                        f"Archive job {archive_job_id} polling exceeded "
                        f"{resolved_timeout}s timeout",
                        archive_job_id=archive_job_id,
                        last_job_state=last_state,
                        last_api_error=last_error,
                    )
                sleep_time = min(backoff, max_backoff_seconds, max(0.0, remaining))
                if sleep_time > 0:
                    jitter = random.uniform(0, min(0.25, sleep_time))
                    time.sleep(sleep_time + jitter)
                backoff = min(backoff * 2, max_backoff_seconds)
                continue

            status = last_state.get("status")
            if status in terminal:
                return last_state

            remaining = resolved_timeout - (time.monotonic() - start)
            sleep_time = min(backoff, max_backoff_seconds, max(0.0, remaining))
            if sleep_time > 0:
                jitter = random.uniform(0, min(0.25, sleep_time))
                time.sleep(sleep_time + jitter)
            backoff = min(backoff * 2, max_backoff_seconds)

    # Pixel Methods
    # These methods delegate to the pixel endpoint

    def get_pixels(
        self,
        adaccount_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get a list of pixels. Delegates to pixel endpoint."""
        return self.pixel.get_pixels(
            adaccount_id=adaccount_id,
            limit=limit,
            offset=offset,
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
