"""
Endpoint modules for the Universal Ads SDK.
"""

from .creative import CreativeEndpoint
from .media import MediaEndpoint
from .report import ReportEndpoint
from .segment import SegmentEndpoint
from .me import MeEndpoint
from .campaign import CampaignEndpoint
from .adset import AdsetEndpoint
from .ad import AdEndpoint
from .pixel import PixelEndpoint

__all__ = [
    "CreativeEndpoint",
    "MediaEndpoint",
    "ReportEndpoint",
    "SegmentEndpoint",
    "MeEndpoint",
    "CampaignEndpoint",
    "AdsetEndpoint",
    "AdEndpoint",
    "PixelEndpoint",
]
