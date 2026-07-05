"""Job queue for async evaluation with SSE streaming support."""
from __future__ import annotations

import asyncio
import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, AsyncGenerator, Optional

from filelock import FileLock


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobStage(str, Enum):
    INIT = "init"
    OWL_ALPHA = "owl_alpha"
    CURSOR_EVAL = "cursor_eval"
    VALIDATING = "validating"
    SAVING = "saving"
    MARKET_SCORING = "market_scoring"
    COMPLETE = "complete"


@dataclass
class EvaluationJob:
    job_id: str
    jd_text: str
    target_role: str
    target_company: Optional[str]
    status: JobStatus = JobStatus.PENDING
    stage: JobStage = JobStage.INIT
    progress: float = 0.0
    message: str = ""
    report: Optional[str] = None
    company: str = ""
    role: str = ""
    report_path: str = ""
    legitimacy: dict = field(default_factory=dict)
    scam_warning: bool = False
    market_score: Optional[int] = None
    market_grade: Optional[str] = None
    top_gaps: list = field(default_factory=list)
    top_strengths: list = field(default_factory=list)
    company_fit: Optional[dict] = None
    error: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "jd_text": self.jd_text,
            "target_role": self.target_role,
            "target_company": self.target_company,
            "status": self.status.value,
            "stage": self.stage.value,
            "progress": self.progress,
            "message": self.message,
            "report": self.report,
            "company": self.company,
            "role": self.role,
            "report_path": self.report_path,
            "legitimacy": self.legitimacy,
            "scam_warning": self.scam_warning,
            "market_score": self.market_score,
            "market_grade": self.market_grade,
            "top_gaps": self.top_gaps,
            "top_strengths": self.top_strengths,
            "company_fit": self.company_fit,
            "error": self.error,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }

    def to_sse_event(self, event_type: str = "stage", content: Optional[str] = None) -> str:
        """Format as SSE data event."""
        payload = {
            "type": event_type,
            "job_id": self.job_id,
            "stage": self.stage.value,
            "progress": self.progress,
            "message": self.message,
        }
        if content is not None:
            payload["content"] = content
        return f"data: {json.dumps(payload)}\n\n"


class JobQueue:
    """File-based job queue with SSE streaming support."""

    def __init__(self, queue_dir: Optional[Path] = None):
        self.queue_dir = queue_dir or Path("/opt/career-ops-dashboard/data/jobs")
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self._lock = FileLock(str(self.queue_dir / "queue.lock"))
        self._jobs: dict[str, EvaluationJob] = {}
        self._subscribers: dict[str, list[asyncio.Queue]] = {}

    def _job_path(self, job_id: str) -> Path:
        return self.queue_dir / f"{job_id}.json"

    def _load_job(self, job_id: str) -> Optional[EvaluationJob]:
        path = self._job_path(job_id)
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        job = EvaluationJob(
            job_id=data["job_id"],
            jd_text=data["jd_text"],
            target_role=data["target_role"],
            target_company=data.get("target_company"),
            status=JobStatus(data["status"]),
            stage=JobStage(data["stage"]),
            progress=data["progress"],
            message=data["message"],
            report=data.get("report"),
            company=data.get("company", ""),
            role=data.get("role", ""),
            report_path=data.get("report_path", ""),
            legitimacy=data.get("legitimacy", {}),
            scam_warning=data.get("scam_warning", False),
            market_score=data.get("market_score"),
            market_grade=data.get("market_grade"),
            top_gaps=data.get("top_gaps", []),
            top_strengths=data.get("top_strengths", []),
            company_fit=data.get("company_fit"),
            error=data.get("error"),
            created_at=data["created_at"],
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
        )
        return job

    def _save_job(self, job: EvaluationJob) -> None:
        path = self._job_path(job.job_id)
        path.write_text(json.dumps(job.to_dict(), indent=2))

    def create_job(
        self,
        jd_text: str,
        target_role: str = "FE-DEV",
        target_company: Optional[str] = None,
    ) -> EvaluationJob:
        job_id = str(uuid.uuid4())[:8]
        job = EvaluationJob(
            job_id=job_id,
            jd_text=jd_text,
            target_role=target_role,
            target_company=target_company,
        )
        with self._lock:
            self._save_job(job)
        return job

    def get_job(self, job_id: str) -> Optional[EvaluationJob]:
        with self._lock:
            return self._load_job(job_id)

    def update_job(self, job: EvaluationJob) -> None:
        """Save job and notify subscribers of stage update."""
        with self._lock:
            self._save_job(job)
            # Notify subscribers
            if job.job_id in self._subscribers:
                for queue in self._subscribers[job.job_id]:
                    try:
                        queue.put_nowait(job.to_sse_event("stage"))
                    except asyncio.QueueFull:
                        pass

    def emit_token(self, job_id: str, content: str) -> None:
        """Emit a token event to subscribers."""
        job = self.get_job(job_id)
        if not job:
            return
        with self._lock:
            if job_id in self._subscribers:
                for queue in self._subscribers[job_id]:
                    try:
                        queue.put_nowait(job.to_sse_event("token", content))
                    except asyncio.QueueFull:
                        pass

    def subscribe(self, job_id: str) -> asyncio.Queue:
        """Subscribe to SSE events for a job."""
        queue = asyncio.Queue(maxsize=100)
        if job_id not in self._subscribers:
            self._subscribers[job_id] = []
        self._subscribers[job_id].append(queue)
        return queue

    def unsubscribe(self, job_id: str, queue: asyncio.Queue) -> None:
        if job_id in self._subscribers and queue in self._subscribers[job_id]:
            self._subscribers[job_id].remove(queue)

    async def stream_events(self, job_id: str) -> AsyncGenerator[str, None]:
        """Stream SSE events for a job."""
        queue = self.subscribe(job_id)
        try:
            # Send initial state
            job = self.get_job(job_id)
            if job:
                yield job.to_sse_event("init")

            while True:
                job = self.get_job(job_id)
                if not job:
                    yield f"data: {json.dumps({'type': 'error', 'message': 'Job not found'})}\n\n"
                    break

                event = await queue.get()
                yield event

                if job.status in (JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED):
                    # Send final event
                    yield job.to_sse_event("complete")
                    break
        finally:
            self.unsubscribe(job_id, queue)


# Global job queue instance
_job_queue: Optional[JobQueue] = None


def get_job_queue() -> JobQueue:
    global _job_queue
    if _job_queue is None:
        _job_queue = JobQueue()
    return _job_queue