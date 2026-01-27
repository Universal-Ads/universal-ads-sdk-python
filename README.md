# Universal Ads SDK

A Python SDK for interacting with the Universal Ads Third Party API. This SDK provides a simple and intuitive interface for managing creatives, uploading media, creating custom segments, and accessing performance reports.

## Features

- **Creative Management**: Create, read, update, and delete creatives
- **Media Upload**: Upload and verify media files
- **Segment Management**: Create and manage custom segments for targeted advertising
- **Reports**: Access campaign, adset, and ad performance data
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

### 2. Upload Media

```python
# Upload a media file (using new API format)
upload_info = client.upload_media(
    mime_type="image/jpeg",
    adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    name="my-image.jpg"
)

# Use the presigned URL to upload your file
import requests
with open("/path/to/your/image.jpg", "rb") as f:
    requests.put(upload_info["upload_url"], data=f)

# Verify the upload
media = client.verify_media(upload_info["id"])
print(f"Media verified: {media['status']}")

# Get media information
media_info = client.get_media(upload_info["id"])
print(f"Media filename: {media_info['filename']}")
```

### 3. Create a Creative

```python
# Create a new creative
creative = client.create_creative(
    adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    name="My Creative",
    media_id="cc0f46c7-d9b9-4758-9479-17e1d77c5eea"
)
print(f"Created creative: {creative['id']}")
```

### 4. Create a Custom Segment

```python
# Option 1: Create segment with uploaded media file
# First, upload a CSV or TXT file containing user identifiers (one per row)
upload_info = client.upload_media(
    mime_type="text/csv",
    adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    name="users.csv"
)

# Upload the file to the presigned URL
import requests
with open("/path/to/users.csv", "rb") as f:
    requests.put(upload_info["upload_url"], data=f)

# Verify the upload
media = client.verify_media(upload_info["id"])

# Create a new custom segment using the uploaded media
segment = client.create_segment(
    adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    name="My Custom Segment",
    segment_type="email",
    media_id=upload_info["id"],
    description="A segment for targeted advertising"
)
print(f"Created segment: {segment['id']}")

# Option 2: Create segment with users list directly (max 10,000 users)
segment = client.create_segment(
    adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    name="My Custom Segment",
    segment_type="email",
    users=["user@example.com", "another@example.com"],
    description="A segment created with user list"
)

# Add or remove users from an existing segment
client.update_segment_users(
    segment_id=segment["id"],
    users=["user@example.com", "another@example.com"],
    remove=False
)
```

### 5. Get Performance Reports

```python
# Get campaign performance report
report = client.get_campaign_report(
    adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    start_date="2024-01-01",
    end_date="2024-01-31",
    date_aggregation="DAY",
    attribution_window="7_day"
)
print(f"Report contains {len(report['data'])} campaigns")

# Schedule an advanced report for asynchronous processing
scheduled_report = client.schedule_report(
    start_date="2024-01-01T00:00:00",
    end_date="2024-01-31T23:59:59",
    entity_level="campaign",
    adaccount_ids=["3d49e08c-465d-4673-a445-d4ba3575f032"],
    dimensions=["state", "dma"],
    time_aggregation="day"
)
print(f"Scheduled report ID: {scheduled_report['scheduled_report_id']}")

# Check scheduled report status
report_status = client.get_scheduled_report(scheduled_report['scheduled_report_id'])
print(f"Report status: {report_status['status']}")
```

### 6. Get Organizations and Ad Accounts

```python
# Get all organizations
organizations = client.get_organizations(limit=50)
print(f"Found {len(organizations['data'])} organizations")

# Get all ad accounts
adaccounts = client.get_adaccounts(limit=50)
print(f"Found {len(adaccounts['data'])} ad accounts")
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
    adaccount_id="account-id",  # Optional: filter by account
    campaign_id="campaign-id",  # Optional: filter by campaign
    adset_id="adset-id",        # Optional: filter by adset
    ad_id="ad-id",              # Optional: filter by ad
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
    adaccount_id="account-id",
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
# New API format
upload_info = client.upload_media(
    mime_type="image/jpeg",
    adaccount_id="account-id",
    name="my-image.jpg"
)


```

#### Get Media
```python
media = client.get_media("media-id")
```

#### Verify Media
```python
media = client.verify_media("media-id")
```

### Reporting

#### Campaign Report
```python
report = client.get_campaign_report(
    adaccount_id="account-id",      # Required
    start_date="2024-01-01",        # Optional
    end_date="2024-01-31",          # Optional
    campaign_ids=["id1", "id2"],   # Optional
    adset_ids=["id1", "id2"],       # Optional
    ad_ids=["id1", "id2"],          # Optional
    date_aggregation="DAY",         # Optional: HOUR, DAY, LIFETIME, TOTAL
    attribution_window="7_day",     # Optional: 7_day, 14_day, 30_day
    limit=100,                      # Optional
    offset=0                        # Optional
)
```

#### Adset Report
```python
report = client.get_adset_report(
    adaccount_id="account-id",      # Required
    start_date="2024-01-01",        # Optional
    end_date="2024-01-31",          # Optional
    campaign_ids=["id1", "id2"],   # Optional
    adset_ids=["id1", "id2"],       # Optional
    ad_ids=["id1", "id2"],          # Optional
    date_aggregation="DAY",          # Optional: HOUR, DAY, LIFETIME, TOTAL
    attribution_window="7_day",      # Optional: 7_day, 14_day, 30_day
    limit=100,                       # Optional
    offset=0                         # Optional
)
```

#### Ad Report
```python
report = client.get_ad_report(
    adaccount_id="account-id",      # Required
    start_date="2024-01-01",        # Optional
    end_date="2024-01-31",          # Optional
    campaign_ids=["id1", "id2"],   # Optional
    adset_ids=["id1", "id2"],       # Optional
    ad_ids=["id1", "id2"],          # Optional
    date_aggregation="DAY",          # Optional: HOUR, DAY, LIFETIME, TOTAL
    attribution_window="7_day",     # Optional: 7_day, 14_day, 30_day
    limit=100,                       # Optional
    offset=0                         # Optional
)
```

#### Schedule Report
```python
scheduled_report = client.schedule_report(
    start_date="2024-01-01T00:00:00",
    end_date="2024-01-31T23:59:59",
    entity_level="campaign",         # campaign, adset, or ad
    adaccount_ids=["account-id"],
    campaign_ids=["id1", "id2"],    # Optional
    adset_ids=["id1", "id2"],       # Optional
    ad_ids=["id1", "id2"],          # Optional
    dimensions=["state", "dma"],     # Optional: device_type, dma, state, zip_code
    time_aggregation="day",          # Optional: hour or day
    limit=50000                      # Optional, default: 100000
)
```

#### Get Scheduled Report
```python
report_status = client.get_scheduled_report("scheduled-report-id")
```

### Segment Management

#### Segment File Format Requirements

When creating or extending segments, you need to upload a media file containing user data. The file must meet these requirements:

- **File Format**: CSV or TXT files only
- **Structure**: Single column format (one identifier per row)
- **Encoding**: UTF-8 encoding
- **File Size**: Maximum 25MB (use `large_files=True` for larger files)
- **Content**: 
  - For email segments: Each row must contain a valid email address
  - For other segment types: Each row contains a single identifier (e.g., IP address, Blockgraph ID, Experian LUID, Liveramp ID)

**Example CSV file for email segments:**
```csv
user1@example.com
user2@example.com
user3@example.com
```

**Example TXT file for email segments:**
```
user1@example.com
user2@example.com
user3@example.com
```

**Upload Process:**
1. Upload your file using the `upload_media()` method to get a `media_id`
2. Use the `media_id` when creating or extending a segment
3. The file will be validated automatically

#### Get All Segments
```python
segments = client.get_segments(
    adaccount_id="account-id",       # Required
    name="Segment Name",             # Optional: filter by name
    status="active",                 # Optional: filter by status
    limit=50,                        # Optional: limit results
    offset=0,                        # Optional: pagination offset
    sort="name_asc"                  # Optional: sort order
)
```

#### Get Specific Segment
```python
segment = client.get_segment("segment-id")
```

#### Create Segment
```python
# Option 1: Create segment with media file
# Note: media_id must reference a CSV or TXT file uploaded via upload_media()
# The file must contain one identifier per row (see Segment File Format Requirements above)
segment = client.create_segment(
    adaccount_id="account-id",
    name="Segment Name",
    segment_type="email",              # email, ctv, ip_address, mobile_ad_id, etc.
    media_id="media-id",                # From upload_media() response
    description="Optional description", # Optional
    large_files=False                   # Optional: set True for files > 25MB
)

# Option 2: Create segment with users list (max 10,000 users)
segment = client.create_segment(
    adaccount_id="account-id",
    name="Segment Name",
    segment_type="email",
    users=["user1@example.com", "user2@example.com"],
    description="Optional description"  # Optional
)
```

#### Update Segment
```python
segment = client.update_segment(
    "segment-id",
    name="Updated Segment Name",
    description="Updated description"    # Optional
)
```

#### Extend Segment
```python
# Add additional media to an existing segment
# Note: media_id must reference a CSV or TXT file uploaded via upload_media()
client.extend_segment(
    segment_id="segment-id",
    media_id="new-media-id",            # From upload_media() response
    large_files=False                    # Optional: set True for files > 25MB
)
```

#### Update Segment Users
```python
# Add users to a segment
client.update_segment_users(
    segment_id="segment-id",
    users=["user1@example.com", "user2@example.com"],
    remove=False  # Set to True to remove users instead
)

# Remove users from a segment
client.update_segment_users(
    segment_id="segment-id",
    users=["user1@example.com"],
    remove=True
)
```

#### Delete Segment
```python
client.delete_segment("segment-id")
```

### Me Endpoints

#### Get Organizations
```python
organizations = client.get_organizations(
    limit=50,    # Optional: limit results (default: 10, max: 100)
    offset=0     # Optional: pagination offset (default: 0)
)
```

#### Get Ad Accounts
```python
adaccounts = client.get_adaccounts(
    limit=50,    # Optional: limit results (default: 10, max: 100)
    offset=0     # Optional: pagination offset (default: 0)
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

The SDK uses request signing for secure API access. Each request is signed with your private key and includes:

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

- Documentation: [https://developers.universalads.com/](https://developers.universalads.com/)
- Issues: [GitHub Issues](https://github.com/universal-ads/universal-ads-sdk-python/issues)
- Email: support+sdk@universalads.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
