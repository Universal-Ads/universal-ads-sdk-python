# Changelog

All notable changes to the Universal Ads SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/universal-ads/universal-ads-sdk-python/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/universal-ads/universal-ads-sdk-python/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/universal-ads/universal-ads-sdk-python/releases/tag/v1.1.0
