# Complete Observability System

> **End-to-End DevOps Observability Platform for Metrics, Logs and Distributed Tracing**

A containerized observability platform built to monitor a Python FastAPI application using **Prometheus, Grafana, Loki, Promtail, Jaeger, OpenTelemetry, Docker and Docker Compose**.

The project demonstrates how application **metrics, logs and distributed traces** can be collected, stored, queried and visualized from a single local environment.

---

## 📌 Project Overview

Modern applications generate three major types of operational data:

* **Metrics** — numerical measurements such as request rate, latency and errors.
* **Logs** — detailed application events and error messages.
* **Traces** — the complete journey of an individual request through an application.

This project integrates these three observability signals into one monitoring platform.

The application intentionally provides normal, slow and error-producing endpoints so that different monitoring scenarios can be demonstrated.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Monitor application performance using **Prometheus**.
2. Visualize metrics using **Grafana**.
3. Centralize application logs using **Loki** and **Promtail**.
4. Trace application requests using **OpenTelemetry and Jaeger**.
5. Run the complete observability stack using **Docker Compose**.
6. Demonstrate normal traffic, slow requests and application errors.
7. Provide a practical DevOps monitoring environment suitable for local development and demonstration.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │   FastAPI App       │
                         │ observability-api   │
                         │    Port: 8000       │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
        ┌───────────┐        ┌────────────┐       ┌──────────────┐
        │Prometheus │        │   Docker   │       │ OpenTelemetry│
        │ Metrics   │        │   Logs     │       │   Tracing    │
        └─────┬─────┘        └──────┬─────┘       └──────┬───────┘
              │                     │                    │
              │                     ▼                    ▼
              │                ┌──────────┐        ┌──────────┐
              │                │ Promtail │        │  Jaeger  │
              │                └────┬─────┘        └──────────┘
              │                     │
              │                     ▼
              │                ┌──────────┐
              │                │   Loki   │
              │                └────┬─────┘
              │                     │
              └──────────────┬──────┘
                             ▼
                       ┌────────────┐
                       │  Grafana   │
                       │ Dashboards │
                       └────────────┘
```

---

# 🔄 Observability Data Flow

## 1. Metrics

```text
FastAPI
   ↓
Prometheus Client
   ↓
/metrics endpoint
   ↓
Prometheus
   ↓
Grafana
```

Prometheus periodically scrapes the FastAPI application's `/metrics` endpoint.

The application exposes metrics including:

* Total HTTP requests
* HTTP request duration
* Requests currently in progress
* Processed orders
* HTTP status codes

---

## 2. Logs

```text
FastAPI
   ↓
Application / Docker Logs
   ↓
Promtail
   ↓
Loki
   ↓
Grafana
```

The application generates structured log messages for important events such as:

```text
Order lookup completed | order_id=12345
```

Promtail collects Docker container logs and forwards them to Loki.

Grafana can then search and filter these logs.

---

## 3. Distributed Tracing

```text
FastAPI
   ↓
OpenTelemetry
   ↓
OTLP
   ↓
Jaeger
```

OpenTelemetry instruments the FastAPI application and sends trace information to Jaeger.

Custom application spans are also created for important operations such as:

* `order-processing`
* `slow-operation`
* `intentional-error`

This makes it possible to investigate the execution of individual requests.

---

# 🧰 Technologies Used

| Technology     | Purpose                             |
| -------------- | ----------------------------------- |
| Python         | Application development             |
| FastAPI        | REST API application                |
| Prometheus     | Metrics collection and querying     |
| Grafana        | Metrics and log visualization       |
| Loki           | Centralized log storage             |
| Promtail       | Log collection                      |
| Jaeger         | Distributed tracing                 |
| OpenTelemetry  | Application instrumentation         |
| Docker         | Containerization                    |
| Docker Compose | Multi-container orchestration       |
| Linux / WSL    | Local development environment       |
| Git / GitHub   | Version control and project hosting |

---

# 📁 Project Structure

```text
observability-platform/
│
├── app/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── main.py
│   └── requirements.txt
│
├── config/
│   │
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   │       ├── dashboards/
│   │       └── datasources/
│   │
│   ├── loki/
│   │   └── loki-config.yml
│   │
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── alerts.yml
│   │
│   └── promtail/
│       └── promtail-config.yml
│
├── docs/
│   ├── architecture.md
│   ├── verification-checklist.md
│   ├── screenshots/
│   └── report/
│
├── scripts/
│
├── screenshots/
│
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

# 🚀 Application Endpoints

The FastAPI application provides several endpoints specifically designed to demonstrate observability.

| Endpoint                 | Purpose                               |
| ------------------------ | ------------------------------------- |
| `/`                      | Application information               |
| `/api/health`            | Health check                          |
| `/api/orders/{order_id}` | Simulates order processing            |
| `/api/slow`              | Generates slow requests               |
| `/api/error`             | Generates intentional HTTP 500 errors |
| `/metrics`               | Prometheus metrics endpoint           |

---

# 📊 Prometheus Metrics

The application exposes custom metrics such as:

### HTTP Request Counter

```text
http_requests_total
```

Tracks HTTP requests using labels such as:

* HTTP method
* API path
* HTTP status

Example:

```text
http_requests_total{
  method="GET",
  path="/api/orders/{order_id}",
  status="200"
}
```

### HTTP Request Duration

```text
http_request_duration_seconds
```

Measures the duration of HTTP requests.

### In-Flight Requests

```text
http_requests_in_flight
```

Tracks requests currently being processed.

### Order Processing Counter

```text
orders_processed_total
```

Tracks successful and failed order-processing operations.

---

# 📝 Centralized Logging

Application logs are collected from Docker containers using Promtail.

Example application log:

```text
2026-09-26 05:51:44,257 | INFO | observability-app |
Order lookup completed | order_id=12345
```

The log pipeline is:

```text
Docker Container
       ↓
Promtail
       ↓
Loki
       ↓
Grafana Explore
```

This allows application events to be searched without manually inspecting individual containers.

---

# 🔭 Distributed Tracing

OpenTelemetry is used to instrument the FastAPI application.

Trace information is exported to Jaeger using OTLP.

Example custom spans include:

```text
order-processing
slow-operation
intentional-error
```

These traces can be used to investigate:

* Request execution
* Slow operations
* Error-producing requests
* Application processing flow

---

# 🚨 Monitoring and Alerting

Prometheus alert rules are configured for important application conditions.

### Application Down

Detects when Prometheus can no longer scrape the application.

```text
ApplicationDown
```

### High Error Rate

Detects when the proportion of HTTP 5xx responses becomes excessive.

```text
HighErrorRate
```

### High Latency

Detects when the application's 95th-percentile latency exceeds the configured threshold.

```text
HighLatency
```

Alert configuration is stored in:

```text
config/prometheus/alerts.yml
```

---

# 🐳 Docker Compose Services

The entire platform runs through Docker Compose.

| Service    |    Port | Role             |
| ---------- | ------: | ---------------- |
| FastAPI    |  `8000` | Demo application |
| Prometheus |  `9090` | Metrics          |
| Grafana    |  `3000` | Visualization    |
| Loki       |  `3100` | Logs             |
| Jaeger     | `16686` | Tracing UI       |
| Promtail   |  `9080` | Log collection   |

All services communicate through the Docker network:

```text
observability
```

---

# ▶️ How to Run the Project

## Prerequisites

Install:

* Docker
* Docker Compose
* Git

Linux/WSL is recommended for the development environment.

---

## 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd observability-platform
```

---

## 2. Start the platform

```bash
docker compose up -d --build
```

---

## 3. Check running containers

```bash
docker compose ps
```

All six services should be running:

```text
app
prometheus
grafana
loki
promtail
jaeger
```

---

# 🌐 Access the Services

After starting the platform:

### FastAPI

```text
http://localhost:8000
```

### FastAPI Health Check

```text
http://localhost:8000/api/health
```

### Prometheus

```text
http://localhost:9090
```

### Grafana

```text
http://localhost:3000
```

Default local credentials:

```text
Username: admin
Password: admin
```

### Loki

```text
http://localhost:3100
```

### Jaeger

```text
http://localhost:16686
```

---

# 🧪 Demonstration Scenarios

The application contains endpoints that allow different observability scenarios to be reproduced.

## Normal Traffic

```bash
for i in {101..110}; do
  curl -s http://localhost:8000/api/orders/$i
done
```

This generates normal application requests, logs and traces.

---

## Slow Requests

```bash
for i in {1..10}; do
  curl -s http://localhost:8000/api/slow > /dev/null
done
```

This generates higher-latency requests that can be investigated through metrics and traces.

---

## Intentional Errors

```bash
for i in {1..10}; do
  curl -s http://localhost:8000/api/error > /dev/null
done
```

This generates HTTP 500 responses and corresponding application logs and traces.

---

# 🔎 Example PromQL Queries

### Total HTTP Requests

```promql
http_requests_total
```

### Request Rate

```promql
sum(rate(http_requests_total[1m]))
```

### HTTP 5xx Rate

```promql
sum(rate(http_requests_total{status=~"5.."}[1m]))
```

### Request Rate by Endpoint

```promql
sum by (path) (rate(http_requests_total[1m]))
```

### 95th Percentile Latency

```promql
histogram_quantile(
  0.95,
  sum(
    rate(http_request_duration_seconds_bucket[1m])
  ) by (le)
)
```

---

# 🔍 Example Loki Query

To search application logs containing the order-processing message:

```logql
{job="docker"} |= "Order lookup completed"
```

To search intentional errors:

```logql
{job="docker"} |= "intentional-error"
```

---

# 📈 Grafana Dashboard

The planned dashboard provides a centralized view of application health and performance.

Dashboard panels include:

* HTTP Request Rate
* HTTP 5xx Error Rate
* 95th Percentile API Latency
* Request Rate by Endpoint
* Total HTTP Requests

Additional Grafana views can be used for:

* Loki application logs
* Jaeger traces
* Error investigation

> Screenshots will be added after the final dashboard and observability scenarios are verified.

---

# 📸 Project Evidence

The final project evidence will include:

```text
screenshots/
│
├── 01-docker-compose-services.png
├── 02-grafana-dashboard.png
├── 03-prometheus-metrics.png
├── 04-loki-logs.png
├── 05-jaeger-traces.png
└── 06-error-monitoring.png
```

These screenshots demonstrate the actual running system rather than simulated results.

---

# 🛠️ Useful Docker Commands

### Start

```bash
docker compose up -d
```

### Rebuild and start

```bash
docker compose up -d --build
```

### Stop

```bash
docker compose down
```

### View service status

```bash
docker compose ps
```

### View application logs

```bash
docker compose logs --tail=50 app
```

### View all service logs

```bash
docker compose logs --tail=50
```

### Restart a service

```bash
docker compose restart <service-name>
```

---

# 🧹 Stop the Platform

To stop the containers:

```bash
docker compose down
```

To stop the containers and remove project volumes:

```bash
docker compose down -v
```

> Removing volumes deletes locally stored Prometheus, Grafana and Loki data.

---

# 🎓 Learning Outcomes

This project provides practical experience with:

* DevOps observability concepts
* Metrics collection
* PromQL
* Centralized logging
* LogQL
* Distributed tracing
* OpenTelemetry
* Grafana visualization
* Docker containerization
* Docker Compose orchestration
* Monitoring application failures
* Performance analysis
* Troubleshooting containerized applications
* Infrastructure configuration
* Git/GitHub project management

---

# 💡 Key DevOps Concepts Demonstrated

### Monitoring

Understanding application health through metrics.

### Logging

Centralizing application events for troubleshooting.

### Tracing

Following individual requests through application operations.

### Alerting

Detecting application failures, high error rates and high latency.

### Observability

Combining **metrics + logs + traces** to understand application behavior.

---

# 📌 Project Status

**Current status: In development / final verification**

### Completed

* FastAPI application
* Docker containerization
* Docker Compose infrastructure
* Prometheus metrics
* Loki configuration
* Promtail log collection
* Grafana data sources
* Jaeger integration
* OpenTelemetry instrumentation
* Demonstration endpoints
* Prometheus alert rules
* Documentation structure

### Finalization

* Grafana dashboard
* Final screenshots
* Trace/log evidence
* GitHub documentation
* Demo video
* Internship report

---

# 👨‍💻 Author

**Harshini**

DevOps / Cloud / Observability Project

---

# 📄 Internship Project

This project was developed as part of a **DevOps internship** and focuses on building an integrated observability system for a containerized application.

The implementation demonstrates the collection and visualization of:

```text
Metrics + Logs + Traces
```

using an entirely Docker-based local environment.

---

## ⭐ Project Summary

```text
FastAPI Application
       │
       ├── Metrics ──────→ Prometheus ──→ Grafana
       │
       ├── Logs ─────────→ Promtail ────→ Loki ──→ Grafana
       │
       └── Traces ───────→ OpenTelemetry → Jaeger
```

**One application. Three observability signals. One integrated DevOps monitoring platform.**
