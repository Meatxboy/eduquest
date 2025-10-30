from __future__ import annotations

import logging
import sys
from typing import Any

import structlog
from prometheus_fastapi_instrumentator import Instrumentator


def setup_logging() -> None:
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

    processors: list[structlog.types.Processor] = [
        structlog.stdlib.add_log_level,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.INFO)


def register_metrics(app: Any) -> None:
    Instrumentator().instrument(app).expose(app, include_in_schema=False)
