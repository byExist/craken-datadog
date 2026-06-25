"""Tests for datadog_mcp.annotations — retention notes injected into descriptions.

``client.get_log_indexes`` is patched so the probe never hits the network: an
index list (or a raised error) drives whether log query tools get a note. The
probe cache is cleared between tests by the autouse fixture (``annotations.reset``
in conftest).
"""

from pytest_mock import MockerFixture

from datadog_mcp import annotations, client, tools
from datadog_mcp.schema.logs import LogsIndex, LogsIndexListResponse


def _patch_indexes(
    mocker: MockerFixture, response: LogsIndexListResponse | None
) -> None:
    annotations.reset()
    if response is None:
        mocker.patch.object(client, "get_log_indexes", side_effect=RuntimeError("boom"))
    else:
        mocker.patch.object(client, "get_log_indexes", return_value=response)


# --- _log_retention_note (cached probe) ---


def test_note_summarizes_indexes(mocker: MockerFixture):
    _patch_indexes(
        mocker,
        LogsIndexListResponse(
            indexes=[
                LogsIndex(
                    name="main", num_retention_days=15, num_flex_logs_retention_days=0
                ),
                LogsIndex(
                    name="audit",
                    num_retention_days=30,
                    num_flex_logs_retention_days=360,
                ),
            ]
        ),
    )

    note = annotations._log_retention_note()

    # flex of 0 means no flex tier, so it is omitted; a positive flex is shown.
    assert note == "Retention by log index: main 15d, audit 30d (+360d flex)."


def test_note_swallows_probe_failure(mocker: MockerFixture):
    _patch_indexes(mocker, None)

    assert annotations._log_retention_note() is None


def test_note_none_when_no_retention_data(mocker: MockerFixture):
    _patch_indexes(mocker, LogsIndexListResponse(indexes=[LogsIndex(name="main")]))

    assert annotations._log_retention_note() is None


def test_note_is_cached(mocker: MockerFixture):
    annotations.reset()
    fn = mocker.patch.object(
        client,
        "get_log_indexes",
        return_value=LogsIndexListResponse(indexes=[]),
    )

    annotations._log_retention_note()
    annotations._log_retention_note()

    fn.assert_called_once()  # probed once, then served from cache


# --- describe ---


def test_describe_appends_retention_to_log_tools(mocker: MockerFixture):
    _patch_indexes(
        mocker,
        LogsIndexListResponse(indexes=[LogsIndex(name="main", num_retention_days=15)]),
    )

    doc = annotations.describe(tools.search_logs)

    assert "Retention by log index: main 15d." in doc
    assert doc.startswith((tools.search_logs.__doc__ or "").rstrip())


def test_describe_uses_static_note_for_span_tools(mocker: MockerFixture):
    _patch_indexes(mocker, LogsIndexListResponse(indexes=[]))

    doc = annotations.describe(tools.search_spans)

    assert "APM spans are kept ~15 days" in doc
    assert doc.startswith((tools.search_spans.__doc__ or "").rstrip())


def test_describe_leaves_other_tools_plain(mocker: MockerFixture):
    _patch_indexes(
        mocker,
        LogsIndexListResponse(indexes=[LogsIndex(name="main", num_retention_days=15)]),
    )

    doc = annotations.describe(tools.list_monitors)

    assert doc == (tools.list_monitors.__doc__ or "").rstrip()


def test_describe_skips_note_when_probe_fails(mocker: MockerFixture):
    _patch_indexes(mocker, None)

    doc = annotations.describe(tools.search_logs)

    assert doc == (tools.search_logs.__doc__ or "").rstrip()
