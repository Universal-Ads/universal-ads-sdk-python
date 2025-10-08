"""
Reporting examples for the Universal Ads SDK.
"""

import os
from datetime import datetime, timedelta
from universal_ads_sdk import UniversalAdsClient, APIError


def get_last_month_reports(client, ad_account_id):
    """
    Get reports for the last month.
    """
    # Calculate last month's date range
    today = datetime.now()
    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)

    start_date = first_day_last_month.strftime("%Y-%m-%d")
    end_date = last_day_last_month.strftime("%Y-%m-%d")

    print(f"Getting reports for {start_date} to {end_date}")

    try:
        # Get campaign report
        print("\n=== Campaign Report ===")
        campaign_report = client.get_campaign_report(
            start_date=start_date,
            end_date=end_date,
            ad_account_id=ad_account_id,
            limit=50,
        )

        campaigns = campaign_report.get("data", [])
        print(f"Found {len(campaigns)} campaigns")

        for campaign in campaigns[:3]:  # Show first 3 campaigns
            print(f"Campaign: {campaign.get('name', 'N/A')}")
            print(f"  ID: {campaign.get('id', 'N/A')}")
            print(f"  Status: {campaign.get('status', 'N/A')}")
            print()

        # Get adset report
        print("\n=== Adset Report ===")
        adset_report = client.get_adset_report(
            start_date=start_date,
            end_date=end_date,
            ad_account_id=ad_account_id,
            limit=50,
        )

        adsets = adset_report.get("data", [])
        print(f"Found {len(adsets)} adsets")

        for adset in adsets[:3]:  # Show first 3 adsets
            print(f"Adset: {adset.get('name', 'N/A')}")
            print(f"  ID: {adset.get('id', 'N/A')}")
            print(f"  Campaign ID: {adset.get('campaign_id', 'N/A')}")
            print()

        # Get ad report
        print("\n=== Ad Report ===")
        ad_report = client.get_ad_report(
            start_date=start_date,
            end_date=end_date,
            ad_account_id=ad_account_id,
            limit=50,
        )

        ads = ad_report.get("data", [])
        print(f"Found {len(ads)} ads")

        for ad in ads[:3]:  # Show first 3 ads
            print(f"Ad: {ad.get('name', 'N/A')}")
            print(f"  ID: {ad.get('id', 'N/A')}")
            print(f"  Adset ID: {ad.get('adset_id', 'N/A')}")
            print()

        return {"campaigns": campaigns, "adsets": adsets, "ads": ads}

    except APIError as e:
        print(f"API error: {e}")
        return None


def get_specific_campaign_report(client, campaign_id, start_date, end_date):
    """
    Get report for a specific campaign.
    """
    try:
        print(f"\n=== Campaign {campaign_id} Report ===")
        report = client.get_campaign_report(
            start_date=start_date, end_date=end_date, campaign_ids=[campaign_id]
        )

        campaigns = report.get("data", [])
        if campaigns:
            campaign = campaigns[0]
            print(f"Campaign: {campaign.get('name', 'N/A')}")
            print(f"Status: {campaign.get('status', 'N/A')}")

            # Print performance metrics if available
            metrics = campaign.get("metrics", {})
            if metrics:
                print("Performance Metrics:")
                for metric, value in metrics.items():
                    print(f"  {metric}: {value}")
        else:
            print("No data found for this campaign")

    except APIError as e:
        print(f"API error: {e}")


def main():
    # Initialize the client
    client = UniversalAdsClient(
        api_key=os.getenv("UNIVERSAL_ADS_API_KEY"),
        private_key_pem=os.getenv("UNIVERSAL_ADS_PRIVATE_KEY"),
    )

    # Example ad account ID - replace with your actual account ID
    ad_account_id = "3d49e08c-465d-4673-a445-d4ba3575f032"

    try:
        # Get last month's reports
        reports = get_last_month_reports(client, ad_account_id)

        if reports and reports["campaigns"]:
            # Get detailed report for the first campaign
            first_campaign = reports["campaigns"][0]
            campaign_id = first_campaign.get("id")

            if campaign_id:
                # Get report for the last 7 days
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

                get_specific_campaign_report(client, campaign_id, start_date, end_date)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
