"""
Media upload example for the Universal Ads SDK.
"""

import os
import requests
from universal_ads_sdk import UniversalAdsClient, APIError


def upload_media_file(client, file_path, content_type):
    """
    Complete example of uploading and verifying a media file.
    """
    try:
        # Step 1: Get upload URL from Universal Ads API
        print(f"Requesting upload URL for {file_path}...")
        upload_info = client.upload_media(
            file_path=file_path, content_type=content_type
        )

        print(f"Got upload URL for media ID: {upload_info['media_id']}")
        print(f"Upload URL: {upload_info['upload_url']}")

        # Step 2: Upload the file to the presigned URL
        print("Uploading file...")
        with open(file_path, "rb") as f:
            upload_response = requests.put(
                upload_info["upload_url"],
                data=f,
                headers={"Content-Type": content_type},
            )
            upload_response.raise_for_status()

        print("File uploaded successfully!")

        # Step 3: Verify the upload with Universal Ads API
        print("Verifying upload...")
        media_info = client.verify_media(upload_info["media_id"])

        print(f"Media verification status: {media_info['status']}")
        print(f"Media ID: {media_info['id']}")

        return media_info

    except APIError as e:
        print(f"API error: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Upload error: {e}")
        return None


def main():
    # Initialize the client
    client = UniversalAdsClient(
        api_key=os.getenv("UNIVERSAL_ADS_API_KEY"),
        private_key_pem=os.getenv("UNIVERSAL_ADS_PRIVATE_KEY"),
    )

    # Example: Upload an image
    image_path = "example_image.jpg"  # Replace with your image path
    if os.path.exists(image_path):
        media_info = upload_media_file(client, image_path, "image/jpeg")

        if media_info:
            print(f"\nSuccessfully uploaded media!")
            print(f"Media ID: {media_info['id']}")
            print(f"Status: {media_info['status']}")
    else:
        print(f"Example image not found: {image_path}")
        print("Please provide a valid image file path to test media upload.")


if __name__ == "__main__":
    main()
