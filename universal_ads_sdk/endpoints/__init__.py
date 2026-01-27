"""
Endpoint modules for the Universal Ads SDK.
"""

from .creative import CreativeEndpoint
from .media import MediaEndpoint
from .report import ReportEndpoint
from .segment import SegmentEndpoint
from .me import MeEndpoint

__all__ = [
    "CreativeEndpoint",
    "MediaEndpoint",
    "ReportEndpoint",
    "SegmentEndpoint",
    "MeEndpoint",
]
