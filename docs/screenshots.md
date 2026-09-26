# Project Evidence and Screenshots

The following screenshots are recommended as evidence for the completed observability platform.

## 1. Grafana Observability Dashboard

File:

`screenshots/01-grafana-observability-dashboard.png`

Shows:

- Total HTTP requests
- API availability
- HTTP request rate
- HTTP 5xx error rate
- 95th percentile latency
- Requests by endpoint
- Application logs

---

## 2. Jaeger Distributed Trace

File:

`screenshots/02-jaeger-distributed-trace.png`

Shows:

- `observability-demo-api`
- Trace timeline
- HTTP request span
- Application processing span
- Span duration

---

## 3. Prometheus Application Down Alert

File:

`screenshots/03-prometheus-application-down-alert.png`

Shows:

- `ApplicationDown`
- Alert state
- Prometheus monitoring the unavailable application

---

## 4. Prometheus High Error Rate Alert

File:

`screenshots/04-prometheus-high-error-rate-alert.png`

Shows:

- `HighErrorRate`
- HTTP 5xx monitoring
- Alert state

---

## 5. Grafana Error Monitoring

File:

`screenshots/05-grafana-error-monitoring.png`

Shows:

- HTTP 5xx activity
- Application error logs
- Observability dashboard response to application failures

---

## Evidence Checklist

- [ ] Grafana dashboard screenshot
- [ ] Jaeger trace screenshot
- [ ] ApplicationDown alert screenshot
- [ ] HighErrorRate alert screenshot
- [ ] Grafana error monitoring screenshot

## Important

Screenshots must be captured from the actual running local environment.

Do not use generated or fabricated screenshots as project evidence.
