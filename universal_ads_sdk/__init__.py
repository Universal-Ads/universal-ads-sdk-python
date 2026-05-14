"""
Universal Ads SDK

A Python SDK for interacting with the Universal Ads Third Party API.
"""

__version__ = "2.2.0"

from .client import UniversalAdsClient
from .common import (
    AdAccountAuthorizationStatus,
    APIError,
    ArchiveAction,
    ArchiveEntityFailureResponse,
    ArchiveEntityResultResponse,
    ArchiveEntityType,
    ArchiveJobResponse,
    ArchiveJobStatus,
    ArchiveJobTimeoutError,
    ArchiveResponse,
    AttributionWindowEnum,
    AudienceStatus,
    AudienceType,
    AuthenticationError,
    EntityLevel,
    PerformanceReportField,
    ReportTimeAggregation,
    ScheduledReportStatus,
    TimeAggregation,
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
    "ArchiveEntityResultResponse",
    "ArchiveEntityFailureResponse",
    "ArchiveJobResponse",
    "ArchiveResponse",
]
