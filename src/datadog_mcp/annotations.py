"""Tool descriptions enriched at registration with the org's data retention.

Retention is config the model needs when it picks a query time window, and it
changes rarely — so we read the log indexes once (cached for the process) and
append each log query tool's effective retention to its docstring. Span tools get
a static note instead: APM retention isn't a single number but a set of sampling
filters over a ~15-day default, so the actionable fact (older spans are a subset)
is constant. The probe degrades to no note on any failure (e.g. an application
key without ``logs_read_config``), so the server still starts and we never assert
a guessed value. Mirrors the role of ``slack.capabilities.describe``.
"""

import logging
from collections.abc import Callable
from functools import lru_cache
from typing import Any

from datadog_mcp import client

logger = logging.getLogger(__name__)

_LOG_RETENTION_TOOLS = frozenset({"search_logs", "aggregate_logs"})
_SPAN_TOOLS = frozenset({"search_spans", "aggregate_spans"})

_SPAN_NOTE = (
    "Retention: APM spans are kept ~15 days by default; past that only spans "
    "matching the org's retention filters are indexed, so older results are a "
    "filtered subset, not the full population."
)


@lru_cache(maxsize=1)
def _log_retention_note() -> str | None:
    """One-line log-index retention summary, probed once; None if undeterminable."""
    try:
        indexes = client.get_log_indexes().indexes or []
    except Exception:
        logger.debug("log index probe failed; skipping retention annotation")
        return None
    parts: list[str] = []
    for index in indexes:
        if index.name is None or index.num_retention_days is None:
            continue
        days = f"{index.num_retention_days}d"
        if index.num_flex_logs_retention_days:
            days += f" (+{index.num_flex_logs_retention_days}d flex)"
        parts.append(f"{index.name} {days}")
    if not parts:
        return None
    return "Retention by log index: " + ", ".join(parts) + "."


def describe(fn: Callable[..., Any]) -> str:
    """Return ``fn``'s docstring with a retention note appended when relevant."""
    doc = (fn.__doc__ or "").rstrip()
    if fn.__name__ in _LOG_RETENTION_TOOLS:
        note = _log_retention_note()
        if note:
            return f"{doc}\n\n{note}"
    elif fn.__name__ in _SPAN_TOOLS:
        return f"{doc}\n\n{_SPAN_NOTE}"
    return doc


def reset() -> None:
    """Clear the cached probe (used to isolate tests)."""
    _log_retention_note.cache_clear()
