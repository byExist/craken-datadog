"""Datadog v1 host schemas (Hosts API)."""

from pydantic import Field

from datadog_mcp.schema.base import DatadogModel

type AgentCheck = list[str]


class HostMetrics(DatadogModel):
    cpu: float | None = None
    iowait: float | None = None
    load: float | None = None


class HostMetaInstallMethod(DatadogModel):
    installer_version: str | None = None
    tool: str | None = None
    tool_version: str | None = None


class HostMeta(DatadogModel):
    agent_checks: list[AgentCheck] | None = None
    agent_version: str | None = None
    cpu_cores: int | None = Field(default=None, alias="cpuCores")
    fbsd_v: list[str] | None = Field(default=None, alias="fbsdV")
    gohai: str | None = None
    install_method: HostMetaInstallMethod | None = None
    mac_v: list[str] | None = Field(default=None, alias="macV")
    machine: str | None = None
    nix_v: list[str] | None = Field(default=None, alias="nixV")
    platform: str | None = None
    processor: str | None = None
    python_v: str | None = Field(default=None, alias="pythonV")
    socket_fqdn: str | None = Field(default=None, alias="socket-fqdn")
    socket_hostname: str | None = Field(default=None, alias="socket-hostname")
    win_v: list[str] | None = Field(default=None, alias="winV")


class Host(DatadogModel):
    aliases: list[str] | None = None
    apps: list[str] | None = None
    aws_name: str | None = None
    host_name: str | None = None
    id: int | None = None
    is_muted: bool | None = None
    last_reported_time: int | None = None
    meta: HostMeta | None = None
    metrics: HostMetrics | None = None
    mute_timeout: int | None = None
    name: str | None = None
    sources: list[str] | None = None
    tags_by_source: dict[str, list[str]] | None = None
    up: bool | None = None


class HostListResponse(DatadogModel):
    host_list: list[Host] | None = None
    total_matching: int | None = None
    total_returned: int | None = None


class HostMuteResponse(DatadogModel):
    action: str | None = None
    end: int | None = None
    hostname: str | None = None
    message: str | None = None


class HostTotals(DatadogModel):
    total_active: int | None = None
    total_up: int | None = None
