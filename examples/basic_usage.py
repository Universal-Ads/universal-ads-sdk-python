"""
Basic usage examples for the Universal Ads SDK.
"""

import os
from universal_ads_sdk import UniversalAdsClient, APIError, AuthenticationError


def main():
    # Initialize the client
    client = UniversalAdsClient(
        api_key=os.getenv("UNIVERSAL_ADS_API_KEY"),
        private_key_pem=os.getenv("UNIVERSAL_ADS_PRIVATE_KEY"),
    )

    try:
        # Example 1: Get all creatives
        print("Fetching creatives...")
        creatives = client.get_creatives(limit=10)
        print(f"Found {len(creatives.get('data', []))} creatives")

        # Example 2: Create a new creative
        print("\nCreating a new creative...")
        new_creative = client.create_creative(
            adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
            name="SDK Test Creative",
            media_id="cc0f46c7-d9b9-4758-9479-17e1d77c5eea",
        )
        print(f"Created creative with ID: {new_creative['id']}")

        # Example 3: Update the creative
        print("\nUpdating the creative...")
        updated_creative = client.update_creative(
            new_creative["id"], name="Updated SDK Test Creative"
        )
        print(f"Updated creative name to: {updated_creative['name']}")

        # Example 4: Get campaign report
        print("\nFetching campaign report...")
        report = client.get_campaign_report(
            start_date="2024-01-01",
            end_date="2024-01-31",
            adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
        )
        print(f"Report contains {len(report.get('data', []))} campaigns")

        # Example 5: Clean up - delete the test creative
        print("\nCleaning up...")
        client.delete_creative(new_creative["id"])
        print("Test creative deleted")

    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except APIError as e:
        print(f"API error {e.status_code}: {e}")
        print(f"Response: {e.response_data}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
