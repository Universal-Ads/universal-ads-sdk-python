"""
Reporting endpoints.
"""

from typing import Dict, Any, Optional
from ._base import BaseEndpoint


class ReportEndpoint(BaseEndpoint):
    """Endpoint for accessing reports."""

    def get_campaign_report(
        self,
        start_date: str,
        end_date: str,
        adaccount_id: Optional[str] = None,
        campaign_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get campaign performance report.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            adaccount_id: Filter by ad account ID
            campaign_ids: List of campaign IDs to include
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Dictionary containing campaign report data
        """
        params = {"start_date": start_date, "end_date": end_date}

        if adaccount_id:
            params["adaccount_id"] = adaccount_id
        if campaign_ids:
            params["campaign_ids"] = campaign_ids
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/report/campaign", params=params)

    def get_adset_report(
        self,
        start_date: str,
        end_date: str,
        adaccount_id: Optional[str] = None,
        adset_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get adset performance report.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            adaccount_id: Filter by ad account ID
            adset_ids: List of adset IDs to include
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Dictionary containing adset report data
        """
        params = {"start_date": start_date, "end_date": end_date}

        if adaccount_id:
            params["adaccount_id"] = adaccount_id
        if adset_ids:
            params["adset_ids"] = adset_ids
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/report/adset", params=params)

    def get_ad_report(
        self,
        start_date: str,
        end_date: str,
        adaccount_id: Optional[str] = None,
        ad_ids: Optional[list] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get ad performance report.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            adaccount_id: Filter by ad account ID
            ad_ids: List of ad IDs to include
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Dictionary containing ad report data
        """
        params = {"start_date": start_date, "end_date": end_date}

        if adaccount_id:
            params["adaccount_id"] = adaccount_id
        if ad_ids:
            params["ad_ids"] = ad_ids
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._make_request("GET", "/report/ad", params=params)
