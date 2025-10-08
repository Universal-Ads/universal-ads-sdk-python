# Universal Ads SDK

A Python SDK for interacting with the Universal Ads Third Party API. This SDK provides a simple and intuitive interface for managing creatives, uploading media, and accessing performance reports.

## Features

- **Creative Management**: Create, read, update, and delete creatives
- **Media Upload**: Upload and verify media files
- **Performance Reports**: Access campaign, adset, and ad performance data
- **Secure Authentication**: ECDSA-based request signing for secure API access
- **Automatic Retries**: Built-in retry logic for robust API interactions
- **Type Hints**: Full type annotation support for better development experience

## Installation

```bash
pip install universal-ads-sdk
```

## Quick Start

### 1. Initialize the Client

```python
from universal_ads_sdk import UniversalAdsClient

# Initialize the client with your API credentials
client = UniversalAdsClient(
    api_key="your-api-key",
    private_key_pem="""-----BEGIN PRIVATE KEY-----
your-private-key-content
-----END PRIVATE KEY-----"""
)
```

### 2. Create a Creative

```python
# Create a new creative
creative = client.create_creative(
    ad_account_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    name="My Creative",
    media_id="cc0f46c7-d9b9-4758-9479-17e1d77c5eea"
)
print(f"Created creative: {creative['id']}")
```

### 3. Upload Media

```python
# Upload a media file
upload_info = client.upload_media(
    file_path="/path/to/your/image.jpg",
    content_type="image/jpeg"
)

# Use the presigned URL to upload your file
import requests
with open("/path/to/your/image.jpg", "rb") as f:
    requests.put(upload_info["upload_url"], data=f)

# Verify the upload
media = client.verify_media(upload_info["media_id"])
print(f"Media verified: {media['status']}")
```

### 4. Get Performance Reports

```python
# Get campaign performance report
report = client.get_campaign_report(
    start_date="2024-01-01",
    end_date="2024-01-31",
    ad_account_id="3d49e08c-465d-4673-a445-d4ba3575f032"
)
print(f"Report contains {len(report['data'])} campaigns")
```

## API Reference

### Client Initialization

```python
UniversalAdsClient(
    api_key: str,                    # Your API key
    private_key_pem: str,            # Your private key in PEM format
    base_url: Optional[str] = None,  # API base URL (defaults to production)
    timeout: int = 30,               # Request timeout in seconds
    max_retries: int = 3             # Maximum retry attempts
)
```

### Creative Management

#### Get All Creatives
```python
creatives = client.get_creatives(
    ad_account_id="account-id",  # Optional: filter by account
    limit=50,                    # Optional: limit results
    offset=0,                    # Optional: pagination offset
    sort="name_asc"              # Optional: sort order
)
```

#### Get Specific Creative
```python
creative = client.get_creative("creative-id")
```

#### Create Creative
```python
creative = client.create_creative(
    ad_account_id="account-id",
    name="Creative Name",
    media_id="media-id"
)
```

#### Update Creative
```python
creative = client.update_creative(
    "creative-id",
    name="New Name"
)
```

#### Delete Creative
```python
client.delete_creative("creative-id")
```

### Media Management

#### Upload Media
```python
upload_info = client.upload_media(
    file_path="/path/to/file",
    content_type="image/jpeg",
    filename="optional-filename.jpg"  # Optional
)
```

#### Verify Media
```python
media = client.verify_media("media-id")
```

### Reporting

#### Campaign Report
```python
report = client.get_campaign_report(
    start_date="2024-01-01",
    end_date="2024-01-31",
    ad_account_id="account-id",      # Optional
    campaign_ids=["id1", "id2"],     # Optional
    limit=100,                       # Optional
    offset=0                         # Optional
)
```

#### Adset Report
```python
report = client.get_adset_report(
    start_date="2024-01-01",
    end_date="2024-01-31",
    ad_account_id="account-id",      # Optional
    adset_ids=["id1", "id2"],        # Optional
    limit=100,                       # Optional
    offset=0                         # Optional
)
```

#### Ad Report
```python
report = client.get_ad_report(
    start_date="2024-01-01",
    end_date="2024-01-31",
    ad_account_id="account-id",      # Optional
    ad_ids=["id1", "id2"],           # Optional
    limit=100,                       # Optional
    offset=0                         # Optional
)
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from universal_ads_sdk import UniversalAdsError, AuthenticationError, APIError

try:
    creative = client.create_creative(...)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except APIError as e:
    print(f"API error {e.status_code}: {e}")
    print(f"Response data: {e.response_data}")
except UniversalAdsError as e:
    print(f"SDK error: {e}")
```

## Configuration

### Environment Variables

You can also initialize the client using environment variables:

```python
import os
from universal_ads_sdk import UniversalAdsClient

client = UniversalAdsClient(
    api_key=os.getenv("UNIVERSAL_ADS_API_KEY"),
    private_key_pem=os.getenv("UNIVERSAL_ADS_PRIVATE_KEY")
)
```

### Custom Base URL

For testing or development, you can use a custom base URL:

```python
client = UniversalAdsClient(
    api_key="your-api-key",
    private_key_pem="your-private-key",
    base_url="https://staging-api.universalads.com/v1"
)
```

## Authentication

The SDK uses ECDSA-based request signing for secure API access. Each request is signed with your private key and includes:

- API key identification
- Timestamp for request freshness
- ECDSA signature for request integrity
- SDK identification headers for logging

## SDK Identification

The SDK automatically includes identification headers in all requests:
- `x-sdk-version`: SDK version number
- `x-sdk-source`: SDK source identifier

These headers help the Universal Ads team identify SDK usage in API logs without requiring any backend changes.

## Requirements

- Python 3.8+
- requests >= 2.25.0
- cryptography >= 3.4.0
- urllib3 >= 1.26.0

## Security

### API Credentials
- **Never commit API credentials to version control**
- Use environment variables for production deployments
- Test files with credentials are excluded from git via `.gitignore`

### Environment Variables (Recommended)
```bash
export UNIVERSAL_ADS_API_KEY="your-api-key"
export UNIVERSAL_ADS_PRIVATE_KEY="your-private-key-pem"
```

```python
import os
from universal_ads_sdk import UniversalAdsClient

client = UniversalAdsClient(
    api_key=os.getenv("UNIVERSAL_ADS_API_KEY"),
    private_key_pem=os.getenv("UNIVERSAL_ADS_PRIVATE_KEY")
)
```

## Development

### Running Tests

The SDK includes test templates in the `tests/` directory. For security, use environment variables:

```bash
# Set up environment variables
cp env.template .env
# Edit .env with your credentials
pip install python-dotenv  # Optional, for better .env support

# Quick test (basic validation)
python tests/test_template.py

# Comprehensive test (all endpoints)
python tests/comprehensive_test.py
```

See `tests/README.md` for detailed testing information.

For development testing with pytest:
```bash
pip install -e ".[dev]"
pytest
```

### Code Formatting

```bash
black universal_ads_sdk/
flake8 universal_ads_sdk/
```

## Support

- Documentation: [https://docs.universalads.com/sdk/python](https://docs.universalads.com/sdk/python)
- Issues: [GitHub Issues](https://github.com/universal-ads/universal-ads-sdk-python/issues)
- Email: support@universalads.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
