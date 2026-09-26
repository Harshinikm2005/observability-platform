import logging
import random
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("observability-app")


# ---------------------------------------------------------
# OpenTelemetry / Jaeger
# ---------------------------------------------------------

resource = Resource.create(
    {
        "service.name": "observability-demo-api",
        "service.version": "1.0.0",
        "deployment.environment": "local",
    }
)

tracer_provider = TracerProvider(resource=resource)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True,
)

tracer_provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer("observability-demo-api")


# ---------------------------------------------------------
# Prometheus Metrics
# ---------------------------------------------------------

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
    buckets=(
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
    ),
)

IN_FLIGHT = Gauge(
    "http_requests_in_flight",
    "Number of HTTP requests currently being processed",
)

ORDERS_PROCESSED = Counter(
    "orders_processed_total",
    "Total number of orders processed",
    ["result"],
)


# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting")
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title="Complete Observability Demo API",
    description="FastAPI service for Prometheus, Loki and Jaeger demonstration",
    version="1.0.0",
    lifespan=lifespan,
)


FastAPIInstrumentor.instrument_app(app)


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def record_request(method: str, path: str, status: int, duration: float):
    REQUEST_COUNT.labels(
        method=method,
        path=path,
        status=str(status),
    ).inc()

    REQUEST_LATENCY.labels(
        method=method,
        path=path,
    ).observe(duration)


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/api/health")
async def health():
    start = time.perf_counter()

    logger.info("Health check requested")

    result = {
        "status": "healthy",
        "service": "observability-demo-api",
        "version": "1.0.0",
    }

    duration = time.perf_counter() - start

    record_request(
        "GET",
        "/api/health",
        200,
        duration,
    )

    return result


# ---------------------------------------------------------
# Orders
# ---------------------------------------------------------

@app.get("/api/orders/{order_id}")
async def get_order(order_id: int):
    start = time.perf_counter()

    with tracer.start_as_current_span("order-processing") as span:
        span.set_attribute("order.id", order_id)

        processing_time = random.uniform(0.02, 0.15)
        time.sleep(processing_time)

        logger.info(
            "Order lookup completed | order_id=%s",
            order_id,
        )

        ORDERS_PROCESSED.labels(result="success").inc()

        response = {
            "order_id": order_id,
            "status": "confirmed",
            "amount": round(random.uniform(100, 5000), 2),
            "currency": "INR",
        }

        span.set_attribute("order.status", "confirmed")

    duration = time.perf_counter() - start

    record_request(
        "GET",
        "/api/orders/{order_id}",
        200,
        duration,
    )

    return response


# ---------------------------------------------------------
# Slow Endpoint
# ---------------------------------------------------------

@app.get("/api/slow")
async def slow_request():
    start = time.perf_counter()

    delay = random.uniform(1.5, 3.5)

    logger.warning(
        "Slow request intentionally triggered | delay=%.2fs",
        delay,
    )

    with tracer.start_as_current_span("slow-operation") as span:
        span.set_attribute("demo.delay_seconds", delay)

        time.sleep(delay)

    duration = time.perf_counter() - start

    record_request(
        "GET",
        "/api/slow",
        200,
        duration,
    )

    return {
        "message": "Slow request completed",
        "delay_seconds": round(delay, 2),
        "duration_seconds": round(duration, 2),
    }


# ---------------------------------------------------------
# Error Endpoint
# ---------------------------------------------------------

@app.get("/api/error")
async def intentional_error():
    start = time.perf_counter()

    with tracer.start_as_current_span("intentional-error") as span:
        span.set_attribute("demo.error", True)

        logger.error(
            "Intentional application error triggered"
        )

        ORDERS_PROCESSED.labels(result="error").inc()

        span.record_exception(
            RuntimeError("Intentional demo failure")
        )

    duration = time.perf_counter() - start

    record_request(
        "GET",
        "/api/error",
        500,
        duration,
    )

    raise HTTPException(
        status_code=500,
        detail="Intentional demo error",
    )


# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------

@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
async def root():
    return {
        "service": "Complete Observability Demo API",
        "status": "running",
        "endpoints": [
            "/api/health",
            "/api/orders/{order_id}",
            "/api/slow",
            "/api/error",
            "/metrics",
        ],
    }
