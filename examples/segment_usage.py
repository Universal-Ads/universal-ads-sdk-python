"""
Segment management examples for the Universal Ads SDK.
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
        # Example 1: Get all segments for an ad account
        print("Fetching segments...")
        adaccount_id = os.getenv("TEST_ADACCOUNT_ID", "your-adaccount-id-here")
        segments = client.get_segments(adaccount_id=adaccount_id, limit=10)
        print(f"Found {len(segments.get('data', []))} segments")

        # Example 2: Get a specific segment
        if segments.get("data"):
            segment_id = segments["data"][0]["id"]
            print(f"\nFetching segment {segment_id}...")
            segment = client.get_segment(segment_id)
            print(f"Segment name: {segment.get('name')}")
            print(f"Segment status: {segment.get('status')}")

        # Example 3: Create a new segment
        print("\nCreating a new segment...")
        media_id = os.getenv("TEST_MEDIA_ID", "your-media-id-here")
        new_segment = client.create_segment(
            adaccount_id=adaccount_id,
            media_id=media_id,
            name="SDK Test Segment",
            segment_type="custom",  # Adjust based on your API's segment types
            description="Test segment created via SDK",
            large_files=False,
        )
        print(f"Created segment with ID: {new_segment['id']}")

        # Example 4: Update the segment
        print("\nUpdating the segment...")
        updated_segment = client.update_segment(
            new_segment["id"],
            name="Updated SDK Test Segment",
            description="Updated description",
        )
        print(f"Updated segment name to: {updated_segment['name']}")

        # Example 5: Extend segment with additional media
        print("\nExtending segment with additional media...")
        extend_media_id = os.getenv("TEST_EXTEND_MEDIA_ID", media_id)
        client.extend_segment(
            segment_id=new_segment["id"],
            media_id=extend_media_id,
            large_files=False,
        )
        print("Segment extended successfully")

        # Example 6: Add users to segment
        print("\nAdding users to segment...")
        test_users = ["user1@example.com", "user2@example.com"]
        client.update_segment_users(
            segment_id=new_segment["id"],
            users=test_users,
            remove=False,
        )
        print(f"Added {len(test_users)} users to segment")

        # Example 7: Remove users from segment
        print("\nRemoving users from segment...")
        client.update_segment_users(
            segment_id=new_segment["id"],
            users=test_users,
            remove=True,
        )
        print(f"Removed {len(test_users)} users from segment")

        # Example 8: Get segments with filters
        print("\nFetching segments with filters...")
        filtered_segments = client.get_segments(
            adaccount_id=adaccount_id,
            name="SDK Test",
            status="active",
            limit=5,
        )
        print(f"Found {len(filtered_segments.get('data', []))} matching segments")

        # Example 9: Clean up - delete the test segment
        print("\nCleaning up...")
        client.delete_segment(new_segment["id"])
        print("Test segment deleted")

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
