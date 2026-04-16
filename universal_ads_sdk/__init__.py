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
    SegmentStatus,
    SegmentType,
    ScheduledReportStatus,
    EntityLevel,
    TimeAggregation,
)

__version__ = "1.3.0"
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
    "SegmentStatus",
    "SegmentType",
    "ScheduledReportStatus",
    "EntityLevel",
    "TimeAggregation",
]
