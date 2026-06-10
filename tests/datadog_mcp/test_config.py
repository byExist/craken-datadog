"""Tests for datadog_mcp.config — settings loaded from DD_* env vars."""

import os

import pytest
from pydantic import ValidationError
from pytest_mock import MockerFixture

from datadog_mcp.config import Auth, get_auth

_CREDS = {
    "DD_API_KEY": "dd-api-secret",
    "DD_APP_KEY": "dd-app-secret",
    "DD_SITE": "datadoghq.eu",
}


def test_auth_reads_credentials_from_env(mocker: MockerFixture):
    mocker.patch.dict(os.environ, _CREDS)

    auth = Auth()  # type: ignore[call-arg]

    assert auth.api_key.get_secret_value() == "dd-api-secret"
    assert auth.app_key.get_secret_value() == "dd-app-secret"
    assert auth.site == "datadoghq.eu"


def test_auth_site_defaults_to_us1(mocker: MockerFixture):
    mocker.patch.dict(os.environ, {"DD_API_KEY": "k", "DD_APP_KEY": "a"})

    assert Auth().site == "datadoghq.com"  # type: ignore[call-arg]


def test_auth_keys_are_masked_in_repr(mocker: MockerFixture):
    mocker.patch.dict(os.environ, _CREDS)

    auth = Auth()  # type: ignore[call-arg]

    assert "dd-api-secret" not in repr(auth)
    assert "dd-app-secret" not in repr(auth)
    assert "dd-api-secret" not in str(auth.api_key)
    assert "dd-app-secret" not in str(auth.app_key)


def test_auth_requires_keys():
    with pytest.raises(ValidationError):
        Auth()  # type: ignore[call-arg]


def test_get_auth_is_cached(mocker: MockerFixture):
    mocker.patch.dict(os.environ, _CREDS)
    get_auth.cache_clear()

    assert get_auth() is get_auth()
