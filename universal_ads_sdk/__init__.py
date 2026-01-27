"""
Universal Ads SDK

A Python SDK for interacting with the Universal Ads Third Party API.
"""

from .client import UniversalAdsClient
from .common import (
    UniversalAdsError,
    AuthenticationError,
    APIError,
    ReportTimeAggregation,
    AttributionWindowEnum,
    SegmentStatus,
    SegmentType,
    ScheduledReportStatus,
    EntityLevel,
    TimeAggregation,
)

__version__ = "1.2.0"
__all__ = [
    "UniversalAdsClient",
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
