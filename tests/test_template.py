#!/usr/bin/env python3
"""
Template test file for Universal Ads SDK

Simple test that validates basic SDK functionality.
Uses environment variables for secure credential management.

Usage:
1. Copy the environment template: cp env.template .env
2. Edit .env with your actual API credentials
3. Load environment variables: source .env
4. Run the test: python tests/test_template.py

DO NOT commit .env files with real credentials to version control.
"""

import sys
import os

# Add the SDK to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv not installed, use system environment variables
    pass

from universal_ads_sdk import UniversalAdsClient, APIError, AuthenticationError

# Load credentials from environment variables
API_KEY = os.getenv("UNIVERSAL_ADS_API_KEY")
PRIVATE_KEY_PEM = os.getenv("UNIVERSAL_ADS_PRIVATE_KEY")


def test_sdk():
    """Test the SDK with your credentials."""
    print("🔍 Testing Universal Ads SDK")
    print("=" * 40)

    try:
        # Initialize client
        print("1. Initializing SDK client...")
        client = UniversalAdsClient(api_key=API_KEY, private_key_pem=PRIVATE_KEY_PEM)
        print("   ✅ Client initialized successfully")

        # Test authentication
        print("2. Testing authentication...")
        try:
            response = client.get_creatives(limit=1)
            print("   ✅ Authentication successful")
        except APIError as e:
            if e.status_code == 422:
                print("   ✅ Authentication successful (422 = missing required params)")
            elif e.status_code == 401:
                print("   ❌ Authentication failed - Check your credentials")
                return False
            else:
                print(f"   ✅ Authentication successful (status {e.status_code})")

        print("\n🎉 SDK test completed successfully!")
        print("   Your SDK is working correctly with your credentials.")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    if not API_KEY or not PRIVATE_KEY_PEM:
        print("❌ API credentials not found in environment variables")
        print("\n📝 Instructions:")
        print("1. Create a .env file in the project root with:")
        print("   UNIVERSAL_ADS_API_KEY=your_api_key_here")
        print("   UNIVERSAL_ADS_PRIVATE_KEY=your_private_key_pem_here")
        print("2. Load the environment variables:")
        print("   source .env  # or use python-dotenv")
        print("3. Run your test: python tests/test_template.py")
        print("\n⚠️  Never commit .env files with real credentials to version control!")
        sys.exit(1)

    success = test_sdk()
    sys.exit(0 if success else 1)
