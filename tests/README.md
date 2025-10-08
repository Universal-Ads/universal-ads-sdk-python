# Universal Ads SDK Tests

This directory contains test files for the Universal Ads SDK.

## ⚠️ Security Notice

**The test files in this directory contain actual API credentials and are excluded from version control for security reasons.**

To run tests with your own credentials, set up environment variables:

1. Copy the environment template: `cp env.template .env`
2. Edit `.env` and add your actual API credentials
3. Install python-dotenv: `pip install python-dotenv` (optional, for better .env support)
4. Run your test: `python tests/comprehensive_test.py`

## Test Files

- **`test_template.py`** - Simple template file for basic testing (safe to commit)
- **`comprehensive_test.py`** - Complete test suite for all SDK functionality (safe to commit)

## Running Tests

### Quick Test (Basic Validation)
```bash
cd /path/to/universal-ads-sdk

# Set up environment variables
cp env.template .env
# Edit .env with your credentials
pip install python-dotenv  # Optional, for better .env support

# Run the simple test
python3 tests/test_template.py
```

### Comprehensive Test (All Endpoints)
```bash
cd /path/to/universal-ads-sdk

# Set up environment variables
cp env.template .env
# Edit .env with your credentials
pip install python-dotenv  # Optional, for better .env support

# Run the comprehensive test
python3 tests/comprehensive_test.py
```

## Test Results

All tests should show that the SDK is working correctly with your API credentials:

- ✅ **SDK Initialization**: Working
- ✅ **Authentication**: Working  
- ✅ **API Connectivity**: Working
- ✅ **Error Handling**: Working

## Notes

- Some tests may show 422 errors (validation errors) - this is expected and indicates the API is reachable
- Some tests may show 403 errors (authorization errors) - this is expected for operations requiring additional permissions
- The SDK is functioning correctly if authentication succeeds (no 401 errors)

## Security Best Practices

### API Credentials
- **Never commit actual API credentials to version control**
- Use the `test_template.py` file to create your own test files
- Store credentials in environment variables or secure configuration files
- The existing test files are excluded from git via `.gitignore`

### Environment Variables (Recommended)
```python
import os
from universal_ads_sdk import UniversalAdsClient

client = UniversalAdsClient(
    api_key=os.getenv("UNIVERSAL_ADS_API_KEY"),
    private_key_pem=os.getenv("UNIVERSAL_ADS_PRIVATE_KEY")
)
```

### Environment Variable Usage
1. Copy `env.template` to `.env`
2. Edit `.env` with your actual credentials
3. Install python-dotenv: `pip install python-dotenv` (optional, for better .env support)
4. Run the test files directly
5. Never commit `.env` files with real credentials
