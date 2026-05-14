"""
Typed shapes for TPA async archive / archive-job API responses.

Runtime values are plain dicts from JSON; these types support static checking.
"""

from typing import List, Optional, TypedDict


class ArchiveEntityResultResponse(TypedDict):
    """Successful entity row from an archive job poll."""

    id: str
    entity_type: str
    name: str


class ArchiveEntityFailureResponse(TypedDict):
    """Failed entity row from an archive job poll."""

    id: str
    entity_type: str
    name: str
    error: str


class ArchiveJobResponse(TypedDict):
    """Response from GET /archive-job/{archive_job_id}."""

    id: str
    status: str
    action: str
    root_entity_type: str
    root_entity_id: str
    root_entity_name: str
    entity_count: int
    entities_processed: int
    entities_remaining: int
    succeeded_entities: List[ArchiveEntityResultResponse]
    failed_entities: List[ArchiveEntityFailureResponse]
    created_at: str
    completed_at: Optional[str]


class ArchiveResponse(TypedDict):
    """Immediate response from POST .../archive or .../unarchive."""

    archive_job_id: str
    polling_timeout_seconds: int
    entity_count: int
