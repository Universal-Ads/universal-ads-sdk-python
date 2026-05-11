"""
Audience management examples for the Universal Ads SDK.
"""

import os
from universal_ads_sdk import UniversalAdsClient, APIError, AuthenticationError


def main():
    # Initialize the client
    client = UniversalAdsClient(
        api_key=os.getenv("UNIVERSAL_ADS_API_KEY"),
        private_key_pem=os.getenv("UNIVERSAL_ADS_PRIVATE_KEY"),
        # For local testing, you can override the base URL:
        # base_url="http://localhost:8000/v1",  # Adjust port as needed
    )

    try:
        # Example 1: Get all audiences for an ad account
        print("Fetching audiences...")
        adaccount_id = os.getenv("TEST_ADACCOUNT_ID", "your-adaccount-id-here")
        audiences = client.get_audiences(adaccount_id=adaccount_id, limit=10)
        print(f"Found {len(audiences.get('data', []))} audiences")

        # Example 2: Get a specific audience
        if audiences.get("data"):
            audience_id = audiences["data"][0]["id"]
            print(f"\nFetching audience {audience_id}...")
            audience = client.get_audience(audience_id)
            print(f"Audience name: {audience.get('name')}")
            print(f"Audience status: {audience.get('status')}")

        # Example 3: Create a new audience with media file
        print("\nCreating a new audience with media file...")
        media_id = os.getenv("TEST_MEDIA_ID", "your-media-id-here")
        new_audience = client.create_audience(
            adaccount_id=adaccount_id,
            name="SDK Test Audience",
            segment_type="email",  # email, ctv, ip_address, mobile_ad_id, etc.
            media_id=media_id,
            description="Test audience created via SDK",
        )
        print(f"Created audience with ID: {new_audience['id']}")

        # Example 3b: Create an audience with users list (alternative to media file)
        print("\nCreating an audience with users list...")
        users_audience = client.create_audience(
            adaccount_id=adaccount_id,
            name="SDK Test Audience (Users)",
            segment_type="email",
            users=["user1@example.com", "user2@example.com"],
            description="Test audience created with users list",
        )
        print(f"Created audience with ID: {users_audience['id']}")

        # Example 4: Update the audience
        print("\nUpdating the audience...")
        updated_audience = client.update_audience(
            new_audience["id"],
            name="Updated SDK Test Audience",
            description="Updated description",
        )
        print(f"Updated audience name to: {updated_audience['name']}")

        # Example 5: Add users via list
        print("\nAdding users to audience...")
        test_users = ["user1@example.com", "user2@example.com"]
        client.update_audience_users(
            audience_id=new_audience["id"],
            users=test_users,
            remove=False,
        )
        print(f"Added {len(test_users)} users to audience")

        # Example 6: Add users via media upload
        print("\nAdding users to audience via media...")
        extend_media_id = os.getenv("TEST_EXTEND_MEDIA_ID", media_id)
        client.update_audience_users(
            audience_id=new_audience["id"],
            media_id=extend_media_id,
            remove=False,
        )
        print("Audience users updated from media successfully")

        # Example 7: Remove users from audience
        print("\nRemoving users from audience...")
        client.update_audience_users(
            audience_id=new_audience["id"],
            users=test_users,
            remove=True,
        )
        print(f"Removed {len(test_users)} users from audience")

        # Example 8: Get audiences with filters
        print("\nFetching audiences with filters...")
        filtered_audiences = client.get_audiences(
            adaccount_id=adaccount_id,
            name="SDK Test",
            status="active",
            limit=5,
        )
        print(f"Found {len(filtered_audiences.get('data', []))} matching audiences")

        # Example 9: Clean up - delete the test audience
        print("\nCleaning up...")
        client.delete_audience(new_audience["id"])
        print("Test audience deleted")

    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except APIError as e:
        print(f"API error {e.status_code}: {e}")
        print(f"Response: {e.response_data}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
