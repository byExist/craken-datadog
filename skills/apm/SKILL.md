---
description: "Investigate Datadog APM — service call volume, errors, and latency from traces and spans. Use for any APM exploration request."
argument-hint: "[keyword] [errors|volume|latency]"
---

# APM Exploration

Narrow from "I don't know the service/env/endpoint" to a concrete span aggregation, four `aggregate_spans` drills deep. Reach for `search_spans` only when counts aren't enough. Default the window to `from_="now-7d"`, `to="now"`.

## Steps

### 1. Find the env

```
aggregate_spans(query="*", compute=[{"aggregation": "count"}], group_by=[{"facet": "env"}])
```

### 2. Find the service

```
aggregate_spans(query="env:{env} service:*{keyword}*", compute=[{"aggregation": "count"}], group_by=[{"facet": "service"}])
```

### 3. Find the entry points

`@_top_level:1` marks the span where a service was entered — tracer-agnostic, and it surfaces non-HTTP entry points too.

```
aggregate_spans(query="env:{env} service:{service} @_top_level:1", compute=[{"aggregation": "count"}], group_by=[{"facet": "operation_name"}])
```

`operation_name` names each entry: HTTP (`servlet.request`, `django.request`, …), queue consumer (`kafka.consume`, …), or scheduled job (`scheduled.call`, …). Pick the one(s) you care about; call it `{op}` below.

### 4. Aggregate by purpose

Keep `operation_name:{op}` in the query — it pins the aggregation to the entry span. Drop it and nested layers (`spring.handler`, DB calls, …) get counted too: requests double-count and `resource_name` mixes routes with bare method names.

```
# Call volume (for errors, add status:error to the query)
aggregate_spans(
  query="env:{env} service:{service} operation_name:{op}",
  compute=[{"aggregation": "count"}],
  group_by=[{"facet": "resource_name", "limit": 20,
             "sort": {"type": "measure", "aggregation": "count", "order": "desc"}}])

# Latency p95 — @duration is in NANOSECONDS (2.07e9 ≈ 2.07s)
aggregate_spans(
  query="env:{env} service:{service} operation_name:{op}",
  compute=[{"aggregation": "pc95", "metric": "@duration"}],
  group_by=[{"facet": "resource_name", "limit": 20,
             "sort": {"type": "measure", "aggregation": "pc95", "metric": "@duration", "order": "desc"}}])
```

## Sampling a raw span (only when counts aren't enough)

A web entry's facets are standard (`resource_name` = `<METHOD> <route>`, `@http.method`, `@http.status_code`, `@duration`), so steps 1→4 need no sample. One span is heavy (full tags + stack trace) — pull one only to:

- learn the facets of a **non-HTTP** entry (`kafka.consume`, `scheduled.call`, …) where there's no `@http.*`;
- read an **actual value** a count can't give — an error message, an example URL, a payload.

```
search_spans(query="env:{env} service:{service} operation_name:{op}", limit=1)
```
