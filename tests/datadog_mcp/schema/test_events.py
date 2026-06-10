from datadog_mcp.schema.events import (
    AlertEventAttributes,
    ChangeEventAttributes,
    EventCreateResponsePayload,
    EventsListResponse,
    V2EventResponse,
)


def test_events_list_response():
    r = EventsListResponse.model_validate(
        {
            "data": [
                {
                    "id": "abc",
                    "type": "event",
                    "attributes": {
                        "message": "m",
                        "tags": ["env:prod"],
                        "timestamp": "2020-05-26T13:36:14Z",
                        "attributes": {
                            "title": "t",
                            "status": "error",
                            "priority": "normal",
                            "monitor_id": 123,
                            "monitor": {"id": 1, "name": "mon"},
                            "evt": {
                                "id": "e1",
                                "name": "n",
                                "source_id": 5,
                                "type": "x",
                            },
                            "date_happened": 1600000000,
                        },
                    },
                }
            ],
            "links": {"next": "https://app.datadoghq.com/x"},
            "meta": {
                "elapsed": 1,
                "status": "done",
                "page": {"after": "c"},
                "warnings": [{"code": "w", "title": "t", "detail": "d"}],
            },
        }
    )
    assert r.data is not None
    er = r.data[0]
    assert er.id == "abc"
    assert er.attributes is not None
    inner = er.attributes.attributes
    assert inner is not None
    assert inner.status == "error"
    assert inner.priority == "normal"
    assert inner.monitor is not None
    assert inner.monitor.name == "mon"
    assert inner.evt is not None
    assert inner.evt.source_id == 5
    assert r.meta is not None
    assert r.meta.warnings is not None
    assert r.meta.warnings[0].code == "w"


def test_v2_event_union_discriminates_alert_and_change():
    alert = V2EventResponse.model_validate(
        {
            "data": {
                "id": "1",
                "type": "event",
                "attributes": {
                    "message": "m",
                    "attributes": {
                        "status": "warn",
                        "priority": "3",
                        "evt": {"category": "alert", "id": "x"},
                        "links": [{"category": "runbook", "title": "rb", "url": "u"}],
                    },
                },
            }
        }
    )
    assert alert.data is not None
    assert alert.data.attributes is not None
    a = alert.data.attributes.attributes
    assert isinstance(a, AlertEventAttributes)
    assert a.status == "warn"
    assert a.links is not None
    assert a.links[0].category == "runbook"

    change = V2EventResponse.model_validate(
        {
            "data": {
                "id": "2",
                "type": "event",
                "attributes": {
                    "message": "m",
                    "attributes": {
                        "changed_resource": {"name": "ff", "type": "feature_flag"},
                        "author": {"name": "me", "type": "user"},
                        "evt": {"category": "change", "id": "y"},
                    },
                },
            }
        }
    )
    assert change.data is not None
    assert change.data.attributes is not None
    c = change.data.attributes.attributes
    assert isinstance(c, ChangeEventAttributes)
    assert c.changed_resource is not None
    assert c.changed_resource.type == "feature_flag"


def test_create_response_self_alias():
    p = EventCreateResponsePayload.model_validate(
        {
            "data": {
                "type": "event",
                "attributes": {"attributes": {"evt": {"id": "i", "uid": "u"}}},
            },
            "links": {"self": "https://app.datadoghq.com/event/1"},
        }
    )
    assert p.links is not None
    assert p.links.self_ == "https://app.datadoghq.com/event/1"
    assert p.data is not None
    assert p.data.attributes is not None
    assert p.data.attributes.attributes is not None
    assert p.data.attributes.attributes.evt is not None
    assert p.data.attributes.attributes.evt.uid == "u"


def test_dump_drops_none():
    dumped = EventsListResponse.model_validate({"meta": {"elapsed": 1}}).model_dump()
    assert dumped == {"meta": {"elapsed": 1}}
