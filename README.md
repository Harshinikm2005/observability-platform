# Complete Observability System

An end-to-end DevOps observability platform providing:

- Metrics with Prometheus
- Dashboards with Grafana
- Centralized logs with Loki
- Distributed tracing with Jaeger
- OpenTelemetry instrumentation
- Docker Compose orchestration

## Project Status

🚧 Under development

## Architecture

FastAPI → Prometheus → Grafana  
FastAPI → Promtail → Loki → Grafana  
FastAPI → OpenTelemetry → Jaeger → Grafana

## Technologies

Python, FastAPI, Docker, Docker Compose, Prometheus, Grafana, Loki, Promtail, Jaeger and OpenTelemetry.
