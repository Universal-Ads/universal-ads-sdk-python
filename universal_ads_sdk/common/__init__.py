"""
Common utilities and shared definitions for the Universal Ads SDK.
"""

from .exceptions import UniversalAdsError, AuthenticationError, APIError
from .types import (
    ReportTimeAggregation,
    AttributionWindowEnum,
    SegmentStatus,
    SegmentType,
    ScheduledReportStatus,
    EntityLevel,
    TimeAggregation,
)

__all__ = [
    "UniversalAdsError",
    "AuthenticationError",
    "APIError",
    "ReportTimeAggregation",
    "AttributionWindowEnum",
    "SegmentStatus",
    "SegmentType",
    "ScheduledReportStatus",
    "EntityLevel",
    "TimeAggregation",
]
