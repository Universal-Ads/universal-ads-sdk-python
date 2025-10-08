"""
Universal Ads SDK

A Python SDK for interacting with the Universal Ads Third Party API.
"""

from .client import UniversalAdsClient
from .exceptions import UniversalAdsError, AuthenticationError, APIError

__version__ = "1.0.0"
__all__ = ["UniversalAdsClient", "UniversalAdsError", "AuthenticationError", "APIError"]
