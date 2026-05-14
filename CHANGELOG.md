# Changelog

All notable changes to the Universal Ads SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-05-14

### Added
- TPA async **archive** and **unarchive** for campaigns, ad sets, and ads (`archive_campaign` / `unarchive_campaign`, `archive_adset` / `unarchive_adset`, `archive_ad` / `unarchive_ad`, plus matching methods on `CampaignEndpoint`, `AdsetEndpoint`, and `AdEndpoint`). Start calls use `POST` with no JSON body.
- **Archive job** polling: `get_archive_job`, `ArchiveJobEndpoint`, and `poll_archive_job` with exponential backoff and jitter until a terminal status or timeout. Application scopes align with backend behavior: **CAMPAIGN_EDIT** for starting archive/unarchive, **CAMPAIGN_READ** for job poll.
- Types: `ArchiveJobStatus`, `ArchiveAction`, `ArchiveEntityType`; TypedDicts `ArchiveResponse`, `ArchiveJobResponse` (including `created_at` / `completed_at` per Connective poll payload), `ArchiveEntityResultResponse`, and `ArchiveEntityFailureResponse`; exception `ArchiveJobTimeoutError` (includes last poll payload and optional last `APIError`).
- Contract tests in `tests/test_archive_job_contract.py` (mocked HTTP).

## [2.1.0] - 2026-05-11

### Changed
- Updated SDK authentication metadata so `x-sdk-version` is sourced from package versioning and now reports `2.1.0`.
- Updated campaign objective support to use `web_conversions` for conversion campaigns and reject legacy `conversions`.
- Aligned campaign/adset/ad/pixel list endpoints with first-class list filters (`campaign_ids`, `adset_ids`, `ad_ids`, `status`, `campaign_type`, `include_archived`) and narrowing pixel list params to API-supported fields.
- Updated SDK list wrappers and request serialization to preserve explicit values such as `offset=0`/`limit=0` by using `is not None` checks.
- Aligned reporting endpoints with backend datetime requirements by enforcing `YYYY-MM-DDTHH:MM:SS` for report date fields.

### Breaking Changes
- `adaccount_id` is now required for `get_campaigns()`, `get_adsets()`, `get_ads()`, and `get_pixels()`.
- Replaced legacy single-ID list filters (`campaign_id`, `adset_id`) with list-based filters (`campaign_ids`, `adset_ids`) on adset/ad list methods; ad list no longer advertises `sort` as a first-class filter parameter.
## [2.0.0] - 2026-05-11

### Removed
- Removed segment endpoint surface from the SDK (`create_segment`, `get_segments`, `get_segment`, `update_segment`, `extend_segment`, `update_segment_users`, `delete_segment`)
- Removed `SegmentEndpoint`, `SegmentStatus`, and `SegmentType` exports

### Added
- Added audience endpoint surface matching latest API spec (`create_audience`, `get_audiences`, `get_audience`, `update_audience`, `update_audience_users`, `delete_audience`)
- Added `AudienceEndpoint`, `AudienceStatus`, and `AudienceType` exports

### Changed
- Migrated endpoint paths from deprecated `/segment` routes to `/audience` routes
- Updated `update_audience_users()` to support both direct user lists and media-based updates (`media_id`)
- Updated docs, examples, and comprehensive tests to audience terminology and API names

## [1.3.0] - 2026-04-16

### Added
- Added campaign resource helpers: `get_campaigns()`, `get_campaign()`, `create_campaign()`, and `update_campaign()`
- Added ad set resource helpers: `get_adsets()`, `get_adset()`, `create_adset()`, and `update_adset()`
- Added ad resource helpers: `get_ads()`, `get_ad()`, `create_ad()`, and `update_ad()`
- Added pixel resource helpers: `get_pixels()`, `get_pixel()`, and `get_pixel_events()`

### Changed
- Extended `get_adaccounts()` to support repeated `organization_id` and `authorization_status` filters
- Extended scheduled report support with `attribution_window` and `time_aggregation="total"`
- Added `AdAccountAuthorizationStatus` and `PerformanceReportField` enums to `common.types`

### Documentation
- Updated `README.md` with campaign/ad set/ad/pixel examples and ad account filter examples

## [1.2.0] - 2025-01-XX

### Added

#### Media Endpoints
- Added `get_media()` method to retrieve media information by ID
- Added support for new API format in `upload_media()` with `mime_type`, `adaccount_id`, and `name` parameters
- Maintained backward compatibility with existing `file_path`/`content_type`/`filename` parameters

#### Creative Endpoints
- Added `campaign_id`, `adset_id`, and `ad_id` query parameters to `get_creatives()` for filtering

#### Report Endpoints
- Added `date_aggregation` parameter to all report methods (HOUR, DAY, LIFETIME, TOTAL)
- Added `adset_ids` parameter to campaign reports
- Added `ad_ids` parameter to campaign and adset reports
- Added `attribution_window` parameter to all report methods (7_day, 14_day, 30_day)
- Added `schedule_report()` method for asynchronous report generation
- Added `get_scheduled_report()` method to check scheduled report status
- Made `adaccount_id` required parameter in all report methods (matching API specification)
- Made `start_date` and `end_date` optional parameters in report methods

#### Segment Endpoints
- Added `users` parameter option to `create_segment()` for programmatic segment creation
- Added validation to ensure either `media_id` or `users` is provided when creating segments
- Added validation to limit users list to maximum 10,000 items

#### Me Endpoints
- Added `get_organizations()` method to retrieve organizations accessible to the authenticated application
- Added `get_adaccounts()` method to retrieve ad accounts accessible to the authenticated application

#### Type System
- Added comprehensive enum classes in `common.types`:
  - `ReportTimeAggregation` - Time aggregation options for reports
  - `AttributionWindowEnum` - Attribution window options
  - `SegmentStatus` - Segment status values
  - `SegmentType` - Segment type values
  - `ScheduledReportStatus` - Scheduled report status values
  - `EntityLevel` - Entity level options for scheduled reports
  - `TimeAggregation` - Time aggregation for scheduled reports
- All enums are exported from the main package for easy access

#### Code Organization
- Reorganized code structure by moving `types.py` and `exceptions.py` to `common/` directory
- Created `common/__init__.py` for centralized exports

### Changed

#### Breaking Changes
- **Report Methods**: `adaccount_id` is now a required parameter (previously optional)
- **Report Methods**: `start_date` and `end_date` are now optional parameters (previously required)
- **Segment Creation**: `media_id` is now optional in `create_segment()` (either `media_id` or `users` must be provided)
- **Media Upload**: New API format uses `mime_type`, `adaccount_id`, `name` (backward compatible wrapper maintained)

#### Non-Breaking Changes
- Updated all report method signatures to match OpenAPI specification
- Improved type hints with enum classes for better IDE support
- Enhanced parameter validation in segment creation

### Documentation
- Updated README.md with all new endpoints and parameters
- Added examples for new functionality (advanced reports, me endpoints, users-based segments)
- Updated all example files to reflect new API usage
- Added comprehensive documentation for enum types

### Internal
- Improved code organization with `common/` package structure
- Enhanced type safety with enum classes
- Better separation of concerns

## [1.1.0] - Previous Release

Initial stable release with basic functionality for:
- Creative management
- Media upload and verification
- Basic reporting
- Segment management

[2.2.0]: https://github.com/universal-ads/universal-ads-sdk-python/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/universal-ads/universal-ads-sdk-python/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/universal-ads/universal-ads-sdk-python/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/universal-ads/universal-ads-sdk-python/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/universal-ads/universal-ads-sdk-python/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/universal-ads/universal-ads-sdk-python/releases/tag/v1.1.0
