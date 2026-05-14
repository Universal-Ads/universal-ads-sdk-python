"""
Common utilities and shared definitions for the Universal Ads SDK.
"""

from .archive_types import (
    ArchiveEntityFailureResponse,
    ArchiveEntityResultResponse,
    ArchiveJobResponse,
    ArchiveResponse,
)
from .exceptions import (
    APIError,
    ArchiveJobTimeoutError,
    AuthenticationError,
    UniversalAdsError,
)
from .types import (
    AdAccountAuthorizationStatus,
    ArchiveAction,
    ArchiveEntityType,
    ArchiveJobStatus,
    AttributionWindowEnum,
    AudienceStatus,
    AudienceType,
    EntityLevel,
    PerformanceReportField,
    ReportTimeAggregation,
    ScheduledReportStatus,
    TimeAggregation,
)

__all__ = [
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
