import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path


_SESSION_ID = None
_SESSION_LOG_PATH = None


def _build_log_path(app_name: str | None) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    pid = os.getpid()
    suffix = uuid.uuid4().hex[:8]
    tag = app_name or "session"
    logs_dir = Path(__file__).resolve().parents[2] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / f"{tag}_{timestamp}_{pid}_{suffix}.log"


def init_session_logging(app_name: str | None = None) -> Path:
    global _SESSION_ID, _SESSION_LOG_PATH
    if _SESSION_LOG_PATH is not None:
        return _SESSION_LOG_PATH

    _SESSION_ID = uuid.uuid4().hex
    _SESSION_LOG_PATH = _build_log_path(app_name)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s [session=%(session_id)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(_SESSION_LOG_PATH, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(_SessionFilterHandler(file_handler))
    logger.addHandler(_SessionFilterHandler(stream_handler))

    logger.info("Logging initialized", extra={"session_id": _SESSION_ID})
    logger.info("Log file created at %s", _SESSION_LOG_PATH, extra={"session_id": _SESSION_ID})
    return _SESSION_LOG_PATH


def get_session_id() -> str | None:
    return _SESSION_ID


def get_log_path() -> Path | None:
    return _SESSION_LOG_PATH


class _SessionFilterHandler(logging.Handler):
    def __init__(self, handler: logging.Handler):
        super().__init__()
        self._handler = handler

    def emit(self, record: logging.LogRecord) -> None:
        if not hasattr(record, "session_id"):
            record.session_id = _SESSION_ID or "unknown"
        self._handler.emit(record)
