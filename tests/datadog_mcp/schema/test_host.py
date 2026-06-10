from datadog_mcp.schema.host import Host, HostListResponse, HostTotals


def test_host_validates_with_aliases():
    h = Host.model_validate(
        {
            "host_name": "i-deadbeef",
            "id": 123456,
            "is_muted": False,
            "meta": {
                "cpuCores": 4,
                "socket-fqdn": "vagrant.vm.",
                "agent_version": "7.32.3",
                "install_method": {"tool": "install_script"},
            },
            "metrics": {"cpu": 99.0, "load": 0.5},
            "tags_by_source": {"Datadog": ["env:prod"]},
        }
    )
    assert h.host_name == "i-deadbeef"
    assert h.meta is not None
    assert h.meta.cpu_cores == 4
    assert h.meta.socket_fqdn == "vagrant.vm."
    assert h.meta.install_method is not None
    assert h.meta.install_method.tool == "install_script"
    assert h.metrics is not None
    assert h.metrics.cpu == 99.0
    assert h.tags_by_source == {"Datadog": ["env:prod"]}


def test_model_dump_drops_none_keys():
    dumped = Host.model_validate({"host_name": "x"}).model_dump()
    assert dumped == {"host_name": "x"}


def test_list_response_nesting():
    r = HostListResponse.model_validate(
        {"host_list": [{"name": "a"}], "total_matching": 1, "total_returned": 1}
    )
    assert r.total_returned == 1
    assert r.host_list is not None
    assert r.host_list[0].name == "a"


def test_host_totals():
    t = HostTotals.model_validate({"total_active": 5, "total_up": 3})
    assert t.total_active == 5
    assert t.total_up == 3
