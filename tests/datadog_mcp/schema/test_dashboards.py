from datadog_mcp.schema.dashboards import Dashboard, DashboardSummary


def test_dashboard_widget_definition_loose():
    d = Dashboard.model_validate(
        {
            "id": "abc-123",
            "title": "API",
            "layout_type": "ordered",
            "description": "desc",
            "tags": ["team:x"],
            "template_variables": [{"name": "env", "prefix": "env", "default": "prod"}],
            "widgets": [
                {
                    "id": 1,
                    "layout": {"x": 0, "y": 0, "width": 4, "height": 2},
                    "definition": {
                        "type": "timeseries",
                        "requests": [{"q": "avg:cpu{*}"}],
                        "title": "CPU",
                    },
                }
            ],
        }
    )
    assert d.id == "abc-123"
    assert d.layout_type == "ordered"
    assert d.widgets is not None
    w = d.widgets[0]
    assert w.id == 1
    assert w.layout is not None
    assert w.layout.width == 4
    assert w.definition == {
        "type": "timeseries",
        "requests": [{"q": "avg:cpu{*}"}],
        "title": "CPU",
    }
    assert d.template_variables is not None
    assert d.template_variables[0].name == "env"


def test_dashboard_summary():
    s = DashboardSummary.model_validate(
        {
            "dashboards": [
                {
                    "id": "d1",
                    "title": "t",
                    "layout_type": "free",
                    "url": "/dashboard/d1",
                }
            ]
        }
    )
    assert s.dashboards is not None
    assert s.dashboards[0].id == "d1"
    assert s.dashboards[0].layout_type == "free"


def test_dump_drops_none():
    dumped = Dashboard.model_validate({"id": "x", "title": "t"}).model_dump()
    assert dumped == {"id": "x", "title": "t"}
