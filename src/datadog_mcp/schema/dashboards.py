"""Datadog v1 dashboard schemas (read; widget definitions left loose).

Widget definitions (the ~100-type oneOf and its query zoo, ~430 schemas) are kept
loose as ``dict`` on ``Widget.definition`` — the data is preserved for reading
without modeling every widget variant. Tabbed-dashboard ``tabs`` are likewise loose.
"""

from typing import Any, Literal

from datadog_mcp.schema.base import DatadogModel

type DashboardLayoutType = Literal["ordered", "free"]
type DashboardReflowType = Literal["auto", "fixed"]


class WidgetLayout(DatadogModel):
    height: int | None = None
    is_column_break: bool | None = None
    width: int | None = None
    x: int | None = None
    y: int | None = None


class Widget(DatadogModel):
    id: int | None = None
    definition: dict[str, Any] | None = None
    layout: WidgetLayout | None = None


class DashboardTemplateVariable(DatadogModel):
    available_values: list[str] | None = None
    default: str | None = None
    defaults: list[str] | None = None
    name: str | None = None
    prefix: str | None = None
    type: str | None = None


class DashboardTemplateVariablePresetValue(DatadogModel):
    name: str | None = None
    value: str | None = None
    values: list[str] | None = None


class DashboardTemplateVariablePreset(DatadogModel):
    name: str | None = None
    template_variables: list[DashboardTemplateVariablePresetValue] | None = None


class Dashboard(DatadogModel):
    author_handle: str | None = None
    author_name: str | None = None
    created_at: str | None = None
    description: str | None = None
    id: str | None = None
    is_read_only: bool | None = None
    layout_type: DashboardLayoutType | None = None
    modified_at: str | None = None
    notify_list: list[str] | None = None
    reflow_type: DashboardReflowType | None = None
    restricted_roles: list[str] | None = None
    tabs: list[dict[str, Any]] | None = None
    tags: list[str] | None = None
    template_variable_presets: list[DashboardTemplateVariablePreset] | None = None
    template_variables: list[DashboardTemplateVariable] | None = None
    title: str | None = None
    url: str | None = None
    widgets: list[Widget] | None = None


class DashboardSummaryDefinition(DatadogModel):
    author_handle: str | None = None
    created_at: str | None = None
    description: str | None = None
    id: str | None = None
    is_read_only: bool | None = None
    layout_type: DashboardLayoutType | None = None
    modified_at: str | None = None
    title: str | None = None
    url: str | None = None


class DashboardSummary(DatadogModel):
    dashboards: list[DashboardSummaryDefinition] | None = None
