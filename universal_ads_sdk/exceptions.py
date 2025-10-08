"""
Custom exceptions for the Universal Ads SDK.
"""


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
