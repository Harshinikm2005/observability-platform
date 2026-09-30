# 🔭 Complete Observability Platform

An end-to-end **DevOps Observability Platform** built using Docker, FastAPI, Prometheus, Grafana, Loki, Promtail, Jaeger, and OpenTelemetry.

This project demonstrates how modern DevOps teams can monitor an application through the three major pillars of observability:

- 📊 **Metrics** – What is happening?
- 📝 **Logs** – Why is it happening?
- 🔎 **Traces** – Where is it happening?

The entire platform runs locally using **Docker Compose**, making it easy to deploy, test, monitor, and demonstrate without requiring any cloud infrastructure.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Objectives](#-objectives)
- [Architecture](#-architecture)
- [Observability Pillars](#-observability-pillars)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Application Features](#-application-features)
- [Metrics Monitoring](#-metrics-monitoring)
- [Centralized Logging](#-centralized-logging)
- [Distributed Tracing](#-distributed-tracing)
- [Alerting](#-alerting)
- [Grafana Dashboard](#-grafana-dashboard)
- [Docker Compose Services](#-docker-compose-services)
- [Installation and Setup](#-installation-and-setup)
- [Running the Project](#-running-the-project)
- [Testing the Application](#-testing-the-application)
- [Verification](#-verification)
- [Screenshots](#-screenshots)
- [Sample Scenarios](#-sample-scenarios)
- [Key Observations](#-key-observations)
- [Challenges and Solutions](#-challenges-and-solutions)
- [Learning Outcomes](#-learning-outcomes)
- [Future Improvements](#-future-improvements)
- [Conclusion](#-conclusion)
- [Author](#-author)

---

# 🚀 Project Overview

Modern applications generate a large amount of operational information.

Simply running an application is not enough. Developers and DevOps engineers need to know:

- Is the application available?
- How many requests are being received?
- Which endpoints are being used?
- How many requests are failing?
- How long are requests taking?
- What errors are occurring?
- What happened before an error occurred?
- Which service or operation caused the delay?

This project addresses these requirements by creating a complete local observability environment.

The platform contains a sample **FastAPI application** and integrates it with:

```text
FastAPI
   │
   ├── Metrics ───────────────► Prometheus ─────► Grafana
   │
   ├── Logs ─► Docker ─► Promtail ─► Loki ─────► Grafana
   │
   └── Traces ─► OpenTelemetry ────────────────► Jaeger
