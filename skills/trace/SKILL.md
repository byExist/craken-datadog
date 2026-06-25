---
description: "Inspect a single Datadog trace by ID — why a request was slow or failed, or what it did and touched. Use when given a trace_id, or asked about a specific request."
argument-hint: "[trace_id]"
---

# Trace Root-Cause

Explain what one request did, or why it was slow or errored, from its trace. Triage cheaply with `aggregate_spans` before fetching the tree — a trace can be thousands of spans, and a fetched tree can overflow the context.

## Steps

### 1. Get the trace_id

If the user gave one, use it. Otherwise surface the exemplar with `search_spans` and read its `trace_id`:

```
search_spans(query="env:{env} service:{service} {filters}", sort="-@duration", limit=1)
```

Slowest → `sort="-@duration"`; a failure → add `status:error`; a specific request → filter by `@http.url`, `@usr.id`, or time.

### 2. Triage cheaply — compose the trace without fetching it

```
aggregate_spans(query="trace_id:{id}", compute=[{"aggregation": "count"}], group_by=[{"facet": "operation_name", "limit": 20, "sort": {"type": "measure", "aggregation": "count", "order": "desc"}}])
```

- The bucket total is the **span count** — your size signal for step 3.
- One operation dominating by count is often the whole answer: many outbound-HTTP spans → external N+1, many DB-query spans → DB N+1. Group by `resource_name` to see *what* repeats.
- For a **failure**, add `status:error` (group by `resource_name`) to pinpoint which spans failed — without fetching the tree.
- Don't attribute time with `sum(@duration)` here — a parent span contains its children, so sums double-count. Use counts.

### 3. Read the causal tree — only when you need structure

```
get_pruned_trace(trace_id="{id}")
```

- **Small trace** → read inline: `root` → `children`, per-span `durationSeconds`, self-time vs children, target hosts in `meta`.
- **Large trace** (thousands of spans — the tree overflows and is saved to a file) → query the file with `jq` over `.data.attributes.summarized_trace.root`:
  - span count — `[recurse(.children[]?)] | length`
  - what dominates — `[recurse(.children[]?) | .name] | group_by(.) | map({name:.[0], n:length}) | sort_by(.n) | reverse`
  - the bottleneck's share — group the dominant spans by `.resource` / `.meta["http.url"]`, sum their `durationSeconds`, compare to `root.durationSeconds`.

## Reading the result

Quantify the cause as its time ÷ the total.

- **Errors** — `error.message`/`error.stack` live in the failing span's `meta`, usually a child, not the root; the step-2 `status:error` aggregate points to it.
- **Self-time** — a span far longer than the sum of its children spent the time itself (body I/O, CPU, an uninstrumented wait), not downstream — the opposite of N+1.
