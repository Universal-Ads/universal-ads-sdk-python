"""
Archive job polling endpoints (TPA async archive / unarchive).
"""

from typing import Any, Dict

from ._base import BaseEndpoint


class ArchiveJobEndpoint(BaseEndpoint):
    """Endpoint for polling async archive job status."""

    def get_archive_job(self, archive_job_id: str) -> Dict[str, Any]:
        """GET /archive-job/{archive_job_id}."""
        return self._make_request("GET", f"/archive-job/{archive_job_id}")
