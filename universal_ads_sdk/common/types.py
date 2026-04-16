"""
Type definitions and enums for the Universal Ads SDK.
"""

from enum import Enum


class ReportTimeAggregation(str, Enum):
    """Time aggregation options for reports."""

    HOUR = "HOUR"
    DAY = "DAY"
    LIFETIME = "LIFETIME"
    TOTAL = "TOTAL"


class AttributionWindowEnum(str, Enum):
    """Attribution window options for reports."""

    SEVEN_DAY = "7_day"
    FOURTEEN_DAY = "14_day"
    THIRTY_DAY = "30_day"


class AdAccountAuthorizationStatus(str, Enum):
    """Authorization status values for ad account filtering."""

    AUTHORIZED = "authorized"
    NOT_AUTHORIZED = "not_authorized"


class PerformanceReportField(str, Enum):
    """Common performance fields accepted by report endpoints."""

    ALL = "all"
    SPEND = "spend"
    IMPRESSIONS = "impressions"
    CLICKS = "clicks"
    CONVERSIONS = "conversions"
    CTR = "ctr"
    CPM = "cpm"
    CPC = "cpc"


class SegmentStatus(str, Enum):
    """Status values for custom segments."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    ELIGIBLE = "ELIGIBLE"
    ERROR = "ERROR"
    DELETED = "DELETED"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"
    EXPIRED = "EXPIRED"


class SegmentType(str, Enum):
    """Type values for custom segments."""

    EMAIL = "email"
    CTV = "ctv"
    IP_ADDRESS = "ip_address"
    MOBILE_AD_ID = "mobile_ad_id"
    WEB_EVENT = "web_event"
    BLOCKGRAPH_ID = "blockgraph_id"
    EXPERIAN_LUID = "experian_luid"
    LIVERAMP_ID = "liveramp_id"


class ScheduledReportStatus(str, Enum):
    """Status values for scheduled reports."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


class EntityLevel(str, Enum):
    """Entity level options for scheduled reports."""

    CAMPAIGN = "campaign"
    ADSET = "adset"
    AD = "ad"


class TimeAggregation(str, Enum):
    """Time aggregation options for scheduled reports."""

    HOUR = "hour"
    DAY = "day"
    TOTAL = "total"
