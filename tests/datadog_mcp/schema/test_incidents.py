from datadog_mcp.schema.incidents import IncidentSearchResponse, IncidentsResponse


def test_incidents_response():
    r = IncidentsResponse.model_validate(
        {
            "data": [
                {
                    "id": "inc1",
                    "type": "incidents",
                    "attributes": {
                        "title": "API outage",
                        "public_id": 42,
                        "severity": "SEV-1",
                        "state": "active",
                        "customer_impacted": True,
                        "customer_impact_duration": 600,
                        "time_to_resolve": 3600,
                        "fields": {"root_cause": {"type": "textbox", "value": "db"}},
                        "notification_handles": [
                            {"handle": "@slack", "display_name": "Slack"}
                        ],
                    },
                    "relationships": {"commander_user": {"data": {"id": "u1"}}},
                }
            ],
            "included": [{"type": "users", "id": "u1"}],
            "meta": {"pagination": {"offset": 0, "size": 10, "next_offset": 10}},
        }
    )
    assert r.data is not None
    inc = r.data[0]
    assert inc.attributes is not None
    assert inc.attributes.title == "API outage"
    assert inc.attributes.severity == "SEV-1"
    assert inc.attributes.customer_impacted is True
    assert inc.attributes.fields == {"root_cause": {"type": "textbox", "value": "db"}}
    assert inc.attributes.notification_handles is not None
    assert inc.attributes.notification_handles[0].handle == "@slack"
    assert inc.relationships == {"commander_user": {"data": {"id": "u1"}}}
    assert r.included is not None
    assert r.included[0]["id"] == "u1"
    assert r.meta is not None
    assert r.meta.pagination is not None
    assert r.meta.pagination.next_offset == 10


def test_incident_search_response():
    r = IncidentSearchResponse.model_validate(
        {
            "data": {
                "type": "incidents_search_results",
                "attributes": {
                    "total": 1,
                    "facets": {"severity": [{"name": "SEV-1", "count": 1}]},
                    "incidents": [
                        {
                            "data": {
                                "id": "inc1",
                                "type": "incidents",
                                "attributes": {"title": "x"},
                            }
                        }
                    ],
                },
            },
            "meta": {"pagination": {"offset": 0, "size": 10}},
        }
    )
    assert r.data is not None
    assert r.data.attributes is not None
    assert r.data.attributes.total == 1
    assert r.data.attributes.facets == {"severity": [{"name": "SEV-1", "count": 1}]}
    assert r.data.attributes.incidents is not None
    inc = r.data.attributes.incidents[0].data
    assert inc is not None
    assert inc.attributes is not None
    assert inc.attributes.title == "x"


def test_dump_drops_none():
    dumped = IncidentsResponse.model_validate(
        {"meta": {"pagination": {"size": 5}}}
    ).model_dump()
    assert dumped == {"meta": {"pagination": {"size": 5}}}
