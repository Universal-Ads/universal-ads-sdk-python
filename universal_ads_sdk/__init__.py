"""
Universal Ads SDK

A Python SDK for interacting with the Universal Ads Third Party API.
"""

from .client import UniversalAdsClient
from .endpoints import CampaignEndpoint, AdsetEndpoint, AdEndpoint, PixelEndpoint
from .common import (
    UniversalAdsError,
    AuthenticationError,
    APIError,
    ReportTimeAggregation,
    AttributionWindowEnum,
    AdAccountAuthorizationStatus,
    PerformanceReportField,
    AudienceStatus,
    AudienceType,
    ScheduledReportStatus,
    EntityLevel,
    TimeAggregation,
)

__version__ = "2.0.0"
__all__ = [
    "UniversalAdsClient",
    "CampaignEndpoint",
    "AdsetEndpoint",
    "AdEndpoint",
    "PixelEndpoint",
    "UniversalAdsError",
    "AuthenticationError",
    "APIError",
    "ReportTimeAggregation",
    "AttributionWindowEnum",
    "AdAccountAuthorizationStatus",
    "PerformanceReportField",
    "AudienceStatus",
    "AudienceType",
    "ScheduledReportStatus",
    "EntityLevel",
    "TimeAggregation",
]
