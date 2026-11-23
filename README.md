# Universal Ads SDK

A Python SDK for interacting with the Universal Ads Third Party API. This SDK provides a simple and intuitive interface for managing campaigns, ad sets, ads, creatives, pixels, media uploads, custom audiences, and performance reports.

## Features

- **Creative Management**: Create, read, update, and delete creatives
- **Campaign, Ad Set, and Ad Management**: List, create, get, and update campaign resources; async archive and unarchive with archive-job polling
- **Pixel Access**: List pixels, get pixel details, and retrieve pixel events
- **Media Upload**: Upload and verify media files
- **Audience Management**: Create and manage custom audiences for targeted advertising
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

### 4. Create a Custom Audience

```python
# Option 1: Create audience with uploaded media file
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

# Create a new custom audience using the uploaded media
audience = client.create_audience(
    adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    name="My Custom Audience",
    segment_type="email",
    media_id=upload_info["id"],
    description="An audience for targeted advertising"
)
print(f"Created audience: {audience['id']}")

# Option 2: Create audience with users list directly (max 10,000 users)
audience = client.create_audience(
    adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    name="My Custom Audience",
    segment_type="email",
    users=["user@example.com", "another@example.com"],
    description="An audience created with user list"
)

# Add or remove users from an existing audience
client.update_audience_users(
    audience_id=audience["id"],
    users=["user@example.com", "another@example.com"],
    remove=False
)
```

### 5. Get Performance Reports

```python
# Get campaign performance report
report = client.get_campaign_report(
    adaccount_id="3d49e08c-465d-4673-a445-d4ba3575f032",
    start_date="2024-01-01T00:00:00",
    end_date="2024-01-31T23:59:59",
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
    max_retries: int = 3,            # Maximum retry attempts
    headers: Optional[Dict[str, str]] = None  # Optional headers added to every request
)
```

This is the signed client. User-token, System User, and access-token clients are under [Authentication](#authentication).

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
    start_date="2024-01-01T00:00:00",  # Optional (YYYY-MM-DDTHH:MM:SS)
    end_date="2024-01-31T23:59:59",    # Optional (YYYY-MM-DDTHH:MM:SS)
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
    start_date="2024-01-01T00:00:00",  # Optional (YYYY-MM-DDTHH:MM:SS)
    end_date="2024-01-31T23:59:59",    # Optional (YYYY-MM-DDTHH:MM:SS)
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
    start_date="2024-01-01T00:00:00",  # Optional (YYYY-MM-DDTHH:MM:SS)
    end_date="2024-01-31T23:59:59",    # Optional (YYYY-MM-DDTHH:MM:SS)
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
    time_aggregation="day",          # Optional: hour, day, or total
    attribution_window="7_day",      # Optional: 7_day, 14_day, 30_day
    limit=50000                      # Optional, default: 100000
)
```

#### Get Scheduled Report
```python
report_status = client.get_scheduled_report("scheduled-report-id")
```

### Campaign Management

#### Get All Campaigns
```python
campaigns = client.get_campaigns(
    adaccount_id="account-id",             # Required
    campaign_ids=["campaign-1"],           # Optional: filter by campaign IDs
    name="Spring Campaign",                # Optional
    status=["active", "paused"],           # Optional: single string also accepted
    campaign_type="performance",           # Optional: performance, content_select
    include_archived=False,                # Optional
    limit=50,                              # Optional
    offset=0,                              # Optional
    sort="id_asc"                          # Optional
)
```

#### Create / Update Campaign
```python
campaign = client.create_campaign(
    adaccount_id="account-id",
    name="Spring Campaign",
    objective="web_conversions"
)

updated = client.update_campaign(campaign["id"], name="Spring Campaign v2")
```

#### Async archive / unarchive (campaign, ad set, ad)

Archive and unarchive run asynchronously. Each start `POST` returns `archive_job_id`, `polling_timeout_seconds`, and `entity_count`. Poll with `get_archive_job` until `status` is `completed`, `partially_failed`, or `failed`, or use `poll_archive_job` with `archive_start_response=start` to apply the suggested timeout from the start response. `poll_archive_job` repeats an `APIError`, including a `401`, until the archive timeout and keeps the same access token. Call `get_archive_job` when a `401` should be retried once with a new client.

```python
start = client.archive_campaign("campaign-uuid")
final = client.poll_archive_job(
    start["archive_job_id"],
    archive_start_response=start,
)

# Ad set and single-ad equivalents
client.unarchive_adset("adset-uuid")
client.archive_ad("ad-uuid")

# One-shot status (no wait)
job = client.get_archive_job("archive-job-uuid")
```

### Ad Set Management

#### Get All Ad Sets
```python
adsets = client.get_adsets(
    adaccount_id="account-id",             # Required
    campaign_ids=["campaign-id"],          # Optional
    adset_ids=["adset-id"],                # Optional
    name="Adults 25-44",                   # Optional
    status=["active", "paused"],           # Optional
    include_archived=False,                # Optional
    limit=50,                              # Optional
    offset=0,                              # Optional
    sort="id_asc"                          # Optional
)
```

#### Create / Update Ad Set
```python
adset = client.create_adset(
    adaccount_id="account-id",
    campaign_id="campaign-id",
    name="Adults 25-44"
)

updated = client.update_adset(adset["id"], name="Adults 25-54")
```

### Ad Management

#### Get All Ads
```python
ads = client.get_ads(
    adaccount_id="account-id",             # Required
    campaign_ids=["campaign-id"],          # Optional
    adset_ids=["adset-id"],                # Optional
    ad_ids=["ad-id"],                      # Optional
    status=["active", "paused"],           # Optional
    include_archived=False,                # Optional
    limit=50,                              # Optional
    offset=0                               # Optional
)
```

#### Create / Update Ad
```python
ad = client.create_ad(
    adaccount_id="account-id",
    adset_id="adset-id",
    creative_id="creative-id",
    name="Homepage Hero Ad"
)

updated = client.update_ad(ad["id"], name="Homepage Hero Ad v2")
```

### Pixel Endpoints

#### Get Pixels
```python
pixels = client.get_pixels(
    adaccount_id="account-id",  # Required
    limit=50,                   # Optional
    offset=0                    # Optional
)
pixel = client.get_pixel("pixel-id")
events = client.get_pixel_events("pixel-id", limit=100, offset=0)
```

### Audience Management

#### Audience File Format Requirements

When creating or updating audiences with `media_id`, you need to upload a media file containing user data. The file must meet these requirements:

- **File Format**: CSV or TXT files only
- **Structure**: Single column format (one identifier per row)
- **Encoding**: UTF-8 encoding
- **File Size**: Maximum 25MB
- **Content**: 
  - For email audiences: Each row must contain a valid email address
  - For other audience types: Each row contains a single identifier (e.g., IP address, Blockgraph ID, Experian LUID, Liveramp ID)

**Example CSV file for email audiences:**
```csv
user1@example.com
user2@example.com
user3@example.com
```

**Example TXT file for email audiences:**
```
user1@example.com
user2@example.com
user3@example.com
```

**Upload Process:**
1. Upload your file using the `upload_media()` method to get a `media_id`
2. Use the `media_id` when creating an audience or updating audience users
3. The file will be validated automatically

#### Get All Audiences
```python
audiences = client.get_audiences(
    adaccount_id="account-id",       # Required
    name="Audience Name",            # Optional: filter by name
    status="active",                 # Optional: filter by status
    limit=50,                        # Optional: limit results
    offset=0,                        # Optional: pagination offset
    sort="name_asc"                  # Optional: sort order
)
```

#### Get Specific Audience
```python
audience = client.get_audience("audience-id")
```

#### Create Audience
```python
# Option 1: Create audience with media file
# Note: media_id must reference a CSV or TXT file uploaded via upload_media()
# The file must contain one identifier per row (see Audience File Format Requirements above)
audience = client.create_audience(
    adaccount_id="account-id",
    name="Audience Name",
    segment_type="email",              # email, ctv, ip_address, mobile_ad_id, etc.
    media_id="media-id",                # From upload_media() response
    description="Optional description", # Optional
)

# Option 2: Create audience with users list (max 10,000 users)
audience = client.create_audience(
    adaccount_id="account-id",
    name="Audience Name",
    segment_type="email",
    users=["user1@example.com", "user2@example.com"],
    description="Optional description"  # Optional
)
```

#### Update Audience
```python
audience = client.update_audience(
    "audience-id",
    name="Updated Audience Name",
    description="Updated description"
)
```

#### Update Audience Users
```python
# Add users to an audience
client.update_audience_users(
    audience_id="audience-id",
    users=["user1@example.com", "user2@example.com"],
    remove=False  # Set to True to remove users instead
)

# Remove users from an audience
client.update_audience_users(
    audience_id="audience-id",
    users=["user1@example.com"],
    remove=True
)

# Update audience users using uploaded media
client.update_audience_users(
    audience_id="audience-id",
    media_id="new-media-id",
    remove=False
)
```

#### Delete Audience
```python
client.delete_audience("audience-id")
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
    limit=50,                                      # Optional: limit results (default: 10, max: 100)
    offset=0,                                      # Optional: pagination offset (default: 0)
    organization_ids=["org-id-1", "org-id-2"],    # Optional: repeatable organization_id query filters
    authorization_statuses=["authorized"]          # Optional: authorized, not_authorized
)
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from universal_ads_sdk import (
    APIError,
    AuthenticationError,
    TokenError,
    TokenStoreError,
    UniversalAdsError,
)

try:
    creative = client.create_creative(...)
except TokenStoreError as e:
    print(f"Store hook failed: {e}")
except TokenError as e:
    print(f"Token error {e.status_code}: {e.error}")
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

Signed clients and token clients call the same methods. Each client uses one credential. Passing signing keys together with OAuth credentials raises `ValueError`.

A token client sends `Authorization: Bearer` and the same `x-sdk-version` and `x-sdk-source` headers as a signed client. `headers=` on a token client cannot set `Authorization`, `x-api-key`, `x-timestamp`, or `x-signature`.

Token requests are `POST {base_url}/oauth/token` as form data. They are not signed and are not retried. The SDK does not follow a redirect from the token endpoint. A refused token request, a redirect, or a token body the SDK cannot read raises `TokenError` with `status_code`, and `error` and `error_description` when the body has them. An API `401` or `403` stays `APIError` and does not request a token.

### Signed client

```python
client = UniversalAdsClient(
    api_key="your-api-key",
    private_key_pem="""-----BEGIN PRIVATE KEY-----
your-private-key-content
-----END PRIVATE KEY-----""",
)
```

Each API request is signed. `headers=` cannot set `x-api-key`, `x-timestamp`, or `x-signature`.

### User token

Send the customer through the authorization redirect and exchange the code yourself, as described on the [User tokens](https://developers.universalads.com/authentication/user-tokens) page. Pass `access_token` and `access_token_expires_at` together, or pass neither. Without that pair, the SDK requests a new access token before the first call.

`access_token_expires_at` is a Unix timestamp in seconds, the same value the store hook receives as `expires_at`. The SDK requests a new access token when the current one expires within 60 seconds (`expires_at - time.time() <= 60`). It uses `expires_in` from the token response, or `access_token_expires_at` when you passed that pair. It does not read the access token.

```python
def store_tokens(access_token, expires_at, refresh_token, scope):
    save(access_token, expires_at, refresh_token)


client = UniversalAdsClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    refresh_token=stored_refresh_token,
    access_token=stored_access_token,
    access_token_expires_at=stored_expires_at,
    store_hook=store_tokens,
)
```

`store_hook` is required. The SDK calls it with the new access token, its expiry, the new refresh token, and `scope` before any API call. The hook must not call this client; that call runs the hook again. If the hook raises, the SDK raises `TokenStoreError` (the hook's exception is `__cause__`), makes no API call, and leaves the new tokens on the client (`access_token`, `access_token_expires_at`, `refresh_token`, and `scope`). The next call runs the hook again with those same values and does not request another token.

When several processes or threads share one customer's user token, hold a lock they share, build the client from the latest stored tokens, and release the lock after the client's calls. The SDK does not take that lock. A System User client needs no lock.

If a refresh fails with `TokenError` and `error` is `invalid_grant`, reread the stored refresh token. When another process has replaced it, build the client from the stored one. Send the customer to authorize the app again only when the stored refresh token is the one that was refused. After a timeout or a 5xx, do not send the customer to authorize again.

If an API call returns `401`, build a new client from the stored refresh token without an access token and repeat the call once. [`poll_archive_job`](#async-archive--unarchive-campaign-ad-set-ad) keeps calling with the same client until its timeout. If that token request is refused, the SDK raises `TokenError`. If the repeated call is refused again, do not retry it. A `403` is not a reason to request a new token.

### System User token

An Owner or Admin authorizes the app for one organization. Store the `system_user_id` from that callback. The steps are on the [System Users](https://developers.universalads.com/authentication/system-users) page. This client sends `grant_type=client_credentials` and `system_user_id`, and it omits `scope`. It takes no refresh token, no access token, and no store hook. For a narrower token, request it as that page shows and pass the access token to the access-token client.

```python
client = UniversalAdsClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    system_user_id="system-user-id",
)
```

Each process can request its own System User token, so this client needs no shared lock. A new client requests a token before the first call. It requests another when that token expires within 60 seconds (`expires_at - time.time() <= 60`), using `expires_in` from the token response.

If an API call returns `401`, build a new System User client and repeat the call once. [`poll_archive_job`](#async-archive--unarchive-campaign-ad-set-ad) keeps calling with the same client until its timeout. If that token request is refused, the SDK raises `TokenError`. If the repeated call is refused again, do not retry it. A `403` is not a reason to request a new token.

### Access token

```python
client = UniversalAdsClient(access_token="access-token")
```

This client sends that access token and never calls the token endpoint.

### Scopes

Scope names are listed on the [Scopes](https://developers.universalads.com/authentication/scopes) page.

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
