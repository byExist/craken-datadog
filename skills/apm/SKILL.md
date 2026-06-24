---
description: "Investigate Datadog APM — service call volume, errors, and latency from traces and spans. Use for any APM exploration request."
argument-hint: "[keyword] [errors|volume|latency]"
---

# APM Exploration

Narrow down from "I don't know the service/env/endpoint" to a concrete span aggregation. `aggregate_spans` drills; `search_spans` pulls one sample to learn the field shape.

Mechanics that bite (verified against the live API):

- `aggregate_spans` ALWAYS requires `compute` — at minimum `[{"aggregation": "count"}]`.
- Percentiles and sum/min/max/avg need a `metric` (the measure facet, e.g. `@duration`). `@duration` is in NANOSECONDS — 2.07e9 ≈ 2.07s.
- To sort buckets by a measure, the `sort` block repeats the same `aggregation` (and `metric` for percentiles).
- Default the window with `from_="now-7d"`, `to="now"` (relative date math; ISO 8601 or epoch ms also work).

Shortcuts — skip ahead when you already know more:

- Know the service and env → jump to step 4.
- Only have a keyword → jump to step 5 and filter with `resource_name:*keyword*` directly.

## Tools

- `aggregate_spans` — the workhorse for every drill-down step
- `search_spans` — pull a single sample span to learn the field shape

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

Group the service's **top-level** spans by `operation_name`. `@_top_level:1` is the tracer-agnostic marker for "the span where this service was entered" — it works for any language/framework and surfaces non-HTTP entry points too.

```
aggregate_spans(query="env:{env} service:{service} @_top_level:1", compute=[{"aggregation": "count"}], group_by=[{"facet": "operation_name"}])
```

A service is often entered more than one way; `operation_name` tells you how:

- HTTP server — `servlet.request` (Spring), `django.request` (Django), `express.request` (Express), `http.request`, … (the exact name varies by tracer)
- Queue consumer — `jms.consume`, `kafka.consume`, …
- Scheduled job — `scheduled.call`, …

Don't assume HTTP — a service can be mostly queue- or cron-driven. Pick the entry operation(s) you care about; call it `{op}` below.

### 4. Inspect one sample for field shape

```
search_spans(query="env:{env} service:{service} operation_name:{op}", limit=1)
```

- For a web entry, `resource_name` is `<METHOD> <normalized route>` — e.g. `GET /orders/{orderId}`.
- Note which facets exist (`@http.method`, `@http.status_code`, `@duration`, …) before grouping by them.

### 5. Aggregate by purpose

Keep `operation_name:{op}` in the query — it pins the aggregation to the entry span. Drop it and the nested layers (`spring.handler`, DB calls, …) get counted too: requests are double-counted and `resource_name` comes back as a mix of routes and bare method names.

```
# Call volume
aggregate_spans(
  query="env:{env} service:{service} operation_name:{op}",
  compute=[{"aggregation": "count"}],
  group_by=[{"facet": "resource_name", "limit": 20,
             "sort": {"type": "measure", "aggregation": "count", "order": "desc"}}])

# Error endpoints, top 20 descending
aggregate_spans(
  query="env:{env} service:{service} operation_name:{op} status:error",
  compute=[{"aggregation": "count"}],
  group_by=[{"facet": "resource_name", "limit": 20,
             "sort": {"type": "measure", "aggregation": "count", "order": "desc"}}])

# Latency (p95) — @duration is in NANOSECONDS
aggregate_spans(
  query="env:{env} service:{service} operation_name:{op}",
  compute=[{"aggregation": "pc95", "metric": "@duration"}],
  group_by=[{"facet": "resource_name", "limit": 20,
             "sort": {"type": "measure", "aggregation": "pc95", "metric": "@duration", "order": "desc"}}])
```

`aggregation` accepts: count, cardinality, sum, min, max, avg, median, pc75, pc90, pc95, pc98, pc99.

## Common filters

- Errors only: `status:error`
- Specific method: `@http.method:DELETE`
- Specific path: `resource_name:*keyword*`
- Status code: `@http.status_code:500`
