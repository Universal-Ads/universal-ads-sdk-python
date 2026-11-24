"""
Universal Ads SDK

A Python SDK for interacting with the Universal Ads Third Party API.
"""

__version__ = "2.3.0"

from .client import UniversalAdsClient
from .common import (
    AdAccountAuthorizationStatus,
    APIError,
    ArchiveAction,
    ArchiveEntityType,
    ArchiveJobStatus,
    ArchiveJobTimeoutError,
    AttributionWindowEnum,
    AudienceStatus,
    AudienceType,
    AuthenticationError,
    EntityLevel,
    PerformanceReportField,
    ReportTimeAggregation,
    ScheduledReportStatus,
    TimeAggregation,
    TokenError,
    TokenStoreError,
    UniversalAdsError,
)
from .endpoints import (
    AdEndpoint,
    AdsetEndpoint,
    ArchiveJobEndpoint,
    CampaignEndpoint,
    PixelEndpoint,
)

__all__ = [
    "UniversalAdsClient",
    "CampaignEndpoint",
    "AdsetEndpoint",
    "AdEndpoint",
    "PixelEndpoint",
    "ArchiveJobEndpoint",
    "UniversalAdsError",
    "AuthenticationError",
    "APIError",
    "TokenError",
    "TokenStoreError",
    "ArchiveJobTimeoutError",
    "ReportTimeAggregation",
    "AttributionWindowEnum",
    "AdAccountAuthorizationStatus",
    "PerformanceReportField",
    "AudienceStatus",
    "AudienceType",
    "ScheduledReportStatus",
    "EntityLevel",
    "TimeAggregation",
    "ArchiveJobStatus",
    "ArchiveAction",
    "ArchiveEntityType",
]
