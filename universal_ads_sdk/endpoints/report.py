"""
Reporting endpoints.
"""

from typing import Dict, Any, Optional, List, Union
from ._base import BaseEndpoint
from ..common.types import (
    ReportTimeAggregation,
    AttributionWindowEnum,
    EntityLevel,
    TimeAggregation,
)


class ReportEndpoint(BaseEndpoint):
    """Endpoint for accessing reports."""

    def get_campaign_report(
        self,
        adaccount_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        campaign_ids: Optional[List[str]] = None,
        adset_ids: Optional[List[str]] = None,
        ad_ids: Optional[List[str]] = None,
        date_aggregation: Optional[Union[ReportTimeAggregation, str]] = None,
        attribution_window: Optional[Union[AttributionWindowEnum, str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get campaign performance report.

        Args:
            adaccount_id: Ad account ID (required)
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            campaign_ids: List of campaign IDs to include
            adset_ids: List of adset IDs to include
            ad_ids: List of ad IDs to include
            date_aggregation: Granularity for the report data aggregation (HOUR, DAY, LIFETIME, TOTAL)
            attribution_window: Attribution window for conversion metrics (7_day, 14_day, 30_day)
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Dictionary containing campaign report data
        """
        params = {"adaccount_id": adaccount_id}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if campaign_ids:
            params["campaign_ids"] = campaign_ids
        if adset_ids:
            params["adset_ids"] = adset_ids
        if ad_ids:
            params["ad_ids"] = ad_ids
        if date_aggregation:
            params["date_aggregation"] = (
                date_aggregation.value
                if isinstance(date_aggregation, ReportTimeAggregation)
                else date_aggregation
            )
        if attribution_window:
            params["attribution_window"] = (
                attribution_window.value
                if isinstance(attribution_window, AttributionWindowEnum)
                else attribution_window
            )
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/report/campaign", params=params)

    def get_adset_report(
        self,
        adaccount_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        campaign_ids: Optional[List[str]] = None,
        adset_ids: Optional[List[str]] = None,
        ad_ids: Optional[List[str]] = None,
        date_aggregation: Optional[Union[ReportTimeAggregation, str]] = None,
        attribution_window: Optional[Union[AttributionWindowEnum, str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get adset performance report.

        Args:
            adaccount_id: Ad account ID (required)
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            campaign_ids: List of campaign IDs to include
            adset_ids: List of adset IDs to include
            ad_ids: List of ad IDs to include
            date_aggregation: Granularity for the report data aggregation (HOUR, DAY, LIFETIME, TOTAL)
            attribution_window: Attribution window for conversion metrics (7_day, 14_day, 30_day)
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Dictionary containing adset report data
        """
        params = {"adaccount_id": adaccount_id}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if campaign_ids:
            params["campaign_ids"] = campaign_ids
        if adset_ids:
            params["adset_ids"] = adset_ids
        if ad_ids:
            params["ad_ids"] = ad_ids
        if date_aggregation:
            params["date_aggregation"] = (
                date_aggregation.value
                if isinstance(date_aggregation, ReportTimeAggregation)
                else date_aggregation
            )
        if attribution_window:
            params["attribution_window"] = (
                attribution_window.value
                if isinstance(attribution_window, AttributionWindowEnum)
                else attribution_window
            )
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/report/adset", params=params)

    def get_ad_report(
        self,
        adaccount_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        campaign_ids: Optional[List[str]] = None,
        adset_ids: Optional[List[str]] = None,
        ad_ids: Optional[List[str]] = None,
        date_aggregation: Optional[Union[ReportTimeAggregation, str]] = None,
        attribution_window: Optional[Union[AttributionWindowEnum, str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get ad performance report.

        Args:
            adaccount_id: Ad account ID (required)
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            campaign_ids: List of campaign IDs to include
            adset_ids: List of adset IDs to include
            ad_ids: List of ad IDs to include
            date_aggregation: Granularity for the report data aggregation (HOUR, DAY, LIFETIME, TOTAL)
            attribution_window: Attribution window for conversion metrics (7_day, 14_day, 30_day)
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Dictionary containing ad report data
        """
        params = {"adaccount_id": adaccount_id}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if campaign_ids:
            params["campaign_ids"] = campaign_ids
        if adset_ids:
            params["adset_ids"] = adset_ids
        if ad_ids:
            params["ad_ids"] = ad_ids
        if date_aggregation:
            params["date_aggregation"] = (
                date_aggregation.value
                if isinstance(date_aggregation, ReportTimeAggregation)
                else date_aggregation
            )
        if attribution_window:
            params["attribution_window"] = (
                attribution_window.value
                if isinstance(attribution_window, AttributionWindowEnum)
                else attribution_window
            )
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/report/ad", params=params)

    def schedule_report(
        self,
        start_date: str,
        end_date: str,
        entity_level: Union[EntityLevel, str],
        adaccount_ids: List[str],
        campaign_ids: Optional[List[str]] = None,
        adset_ids: Optional[List[str]] = None,
        ad_ids: Optional[List[str]] = None,
        dimensions: Optional[List[str]] = None,
        time_aggregation: Optional[Union[TimeAggregation, str]] = None,
        attribution_window: Optional[Union[AttributionWindowEnum, str]] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Schedule a report for asynchronous processing.

        Args:
            start_date: Start date for the report (YYYY-MM-DDTHH:MM:SS format)
            end_date: End date for the report (YYYY-MM-DDTHH:MM:SS format)
            entity_level: Entity level for the report (campaign, adset, or ad)
            adaccount_ids: List of ad account IDs (required)
            campaign_ids: Optional list of campaign IDs
            adset_ids: Optional list of adset IDs
            ad_ids: Optional list of ad IDs
            dimensions: Optional dimensions to group by (device_type, dma, state, zip_code)
            time_aggregation: Time aggregation (hour, day, or total)
            attribution_window: Attribution window for conversion metrics (7_day, 14_day, 30_day)
            limit: Maximum number of rows (default: 100000)

        Returns:
            Dictionary containing scheduled report information
        """
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "entity_level": (
                entity_level.value
                if isinstance(entity_level, EntityLevel)
                else entity_level
            ),
            "adaccount_ids": adaccount_ids,
        }

        if campaign_ids:
            data["campaign_ids"] = campaign_ids
        if adset_ids:
            data["adset_ids"] = adset_ids
        if ad_ids:
            data["ad_ids"] = ad_ids
        if dimensions:
            data["dimensions"] = dimensions
        if time_aggregation:
            data["time_aggregation"] = (
                time_aggregation.value
                if isinstance(time_aggregation, TimeAggregation)
                else time_aggregation
            )
        if attribution_window:
            data["attribution_window"] = (
                attribution_window.value
                if isinstance(attribution_window, AttributionWindowEnum)
                else attribution_window
            )
        if limit:
            data["limit"] = limit

        return self._make_request("POST", "/report/advanced_report", data=data)

    def get_scheduled_report(self, scheduled_report_id: str) -> Dict[str, Any]:
        """
        Get information about a scheduled report.

        Args:
            scheduled_report_id: Unique identifier of the scheduled report (UUID)

        Returns:
            Dictionary containing scheduled report status and information
        """
        return self._make_request(
            "GET", f"/report/advanced_report/{scheduled_report_id}"
        )
