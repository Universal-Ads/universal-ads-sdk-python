"""
Custom exceptions for the Universal Ads SDK.
"""

from typing import Optional


class UniversalAdsError(Exception):
    """Base exception for all Universal Ads SDK errors."""

    pass


class AuthenticationError(UniversalAdsError):
    """Raised when authentication fails."""

    pass


class APIError(UniversalAdsError):
    """Raised when an API request fails."""

    def __init__(
        self, message: str, status_code: int = None, response_data: dict = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class ArchiveJobTimeoutError(UniversalAdsError):
    """Raised when polling an archive job exceeds the allowed duration."""

    def __init__(
        self,
        message: str,
        *,
        archive_job_id: str,
        last_job_state: dict = None,
        last_api_error: Optional[APIError] = None,
    ):
        super().__init__(message)
        self.archive_job_id = archive_job_id
        self.last_job_state = last_job_state or {}
        self.last_api_error = last_api_error
