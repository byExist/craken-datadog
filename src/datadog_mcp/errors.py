"""Datadog API error handling.

A single httpx response hook turns any non-2xx into a ``DatadogError`` that
surfaces Datadog's ``{"errors": [...]}`` envelope, so the model sees what
actually failed rather than a bare status line. A 403 carries an extra note: the
application key lacks the required permission and retrying will not help.
"""

from typing import cast

import httpx


class DatadogError(Exception):
    def __init__(self, status: int, messages: list[str]) -> None:
        self.status = status
        self.messages = messages
        detail = "; ".join(messages) or "(no detail)"
        super().__init__(f"Datadog returned {status}: {detail}")


def _messages(response: httpx.Response) -> list[str]:
    try:
        body: object = response.json()
    except ValueError:
        return [response.text] if response.text else []
    if isinstance(body, dict):
        errors = cast("dict[str, object]", body).get("errors")
        if isinstance(errors, list):
            return [str(item) for item in cast("list[object]", errors)]
    return []


def error_hook(response: httpx.Response) -> None:
    if response.is_success:
        return
    response.read()
    messages = _messages(response)
    if response.status_code == 403:
        messages.append(
            "Do not retry; tell the user their Datadog application key lacks the "
            "permission or scope for this action."
        )
    raise DatadogError(response.status_code, messages)
