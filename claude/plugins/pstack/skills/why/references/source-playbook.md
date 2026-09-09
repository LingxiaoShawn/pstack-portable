# Source playbooks

Choose sources for a specific unresolved question. These playbooks provide
examples for common tools; adapt the queries to actual available interfaces and
read only relevant sections. They do not require one worker per category.

| Question | Playbook | Typical source |
|---|---|---|
| What motivated the implementation? | [Code archaeology](sources/code-archaeology.md) | Git and PR history |
| What requirement drove it? | [Issue tracker](sources/linear.md) | Linked issue |
| Where was the design explained? | [Documents](sources/notion.md) | Design document |
| Where was a tradeoff discussed? | [Discussion](sources/slack.md) | Relevant team thread |
| What runtime condition drove it? | [Observability](sources/datadog.md) | Metrics, logs, traces |
| Which failure prompted it? | [Errors](sources/sentry.md) | Error record |
| Where did a numeric threshold come from? | [Analytics](sources/databricks.md) | Relevant data query |

Use [incident-postmortem.md](sources/incident-postmortem.md) when incident history
could resolve the question. A null check or retry alone does not require an
incident investigation. Follow only leads relevant to the scoped question and
stop when the evidence is sufficient or the search limit is reached.
