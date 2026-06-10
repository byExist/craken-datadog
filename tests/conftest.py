"""Shared test fixtures.

``isolate_env`` (autouse) snapshots and clears ``DD_*`` env vars and resets the
client singleton around every test, so a developer's real Datadog config never
leaks in. ``datadog_api`` wires a ``support.MockServer`` into the client through
an ``httpx.MockTransport`` and patches ``get_auth`` with dummy credentials, so
tests set per-route responses and assert on the requests made. All patching goes
through pytest-mock's ``mocker``.
"""

import os
from typing import Any

import httpx
import pytest
from pytest_mock import MockerFixture
from support import MockServer

from datadog_mcp import client as datadog_client
from datadog_mcp.config import Auth, get_auth

_REAL_HTTPX_CLIENT = httpx.Client

_FAKE_AUTH = Auth(
    api_key="dd-api-test",  # type: ignore[arg-type]
    app_key="dd-app-test",  # type: ignore[arg-type]
    site="datadoghq.com",
)

_DD_ENV = ("DD_API_KEY", "DD_APP_KEY", "DD_SITE")


@pytest.fixture(autouse=True)
def isolate_env(mocker: MockerFixture) -> None:
    mocker.patch.dict(os.environ)
    for var in _DD_ENV:
        os.environ.pop(var, None)
    get_auth.cache_clear()
    mocker.patch.object(datadog_client, "_client", None)


@pytest.fixture
def datadog_api(mocker: MockerFixture) -> MockServer:
    server = MockServer()
    mocker.patch.object(datadog_client, "_client", None)
    mocker.patch.object(datadog_client, "get_auth", lambda: _FAKE_AUTH)

    def factory(**kwargs: Any) -> httpx.Client:
        kwargs.setdefault("transport", httpx.MockTransport(server.handler))
        return _REAL_HTTPX_CLIENT(**kwargs)

    mocker.patch.object(datadog_client.httpx, "Client", factory)
    return server
