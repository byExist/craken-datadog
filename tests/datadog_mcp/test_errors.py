import pytest
from support import MockServer

from datadog_mcp.client import search_logs
from datadog_mcp.errors import DatadogError


def test_error_surfaces_messages(datadog_api: MockServer):
    datadog_api.add(
        "POST",
        "/api/v2/logs/events/search",
        status=400,
        json={"errors": ["Invalid query"]},
    )

    with pytest.raises(DatadogError) as exc:
        search_logs("???")

    assert exc.value.status == 400
    assert exc.value.messages == ["Invalid query"]
    assert "Invalid query" in str(exc.value)


def test_error_403_adds_permission_note(datadog_api: MockServer):
    datadog_api.add(
        "POST", "/api/v2/logs/events/search", status=403, json={"errors": ["Forbidden"]}
    )

    with pytest.raises(DatadogError) as exc:
        search_logs("*")

    assert exc.value.status == 403
    assert "Forbidden" in exc.value.messages
    assert "application key" in str(exc.value).lower()


def test_error_non_json_falls_back_to_text(datadog_api: MockServer):
    datadog_api.add(
        "POST", "/api/v2/logs/events/search", status=502, text="bad gateway"
    )

    with pytest.raises(DatadogError) as exc:
        search_logs("*")

    assert exc.value.status == 502
    assert "bad gateway" in str(exc.value)


def test_error_no_detail(datadog_api: MockServer):
    datadog_api.add("POST", "/api/v2/logs/events/search", status=500, json={})

    with pytest.raises(DatadogError) as exc:
        search_logs("*")

    assert exc.value.status == 500
    assert "(no detail)" in str(exc.value)
