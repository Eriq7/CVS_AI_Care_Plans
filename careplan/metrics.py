from prometheus_client import Counter, Histogram, Gauge

# ── Business Metrics ──────────────────────────────────────

careplan_requests_total = Counter(
    'careplan_requests_total',
    'Total care plan generation requests',
    ['status'],
)

careplan_status_total = Counter(
    'careplan_status_total',
    'Total care plans reaching terminal status',
    ['status'],
)

careplan_active_count = Gauge(
    'careplan_active_count',
    'Current care plans by status',
    ['status'],
)

careplan_duplicate_blocks_total = Counter(
    'careplan_duplicate_blocks_total',
    'Requests blocked due to duplicate detection',
    ['reason'],
)

# ── Performance Metrics ───────────────────────────────────

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint', 'status_code'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0],
)

careplan_generation_duration_seconds = Histogram(
    'careplan_generation_duration_seconds',
    'Total time to generate a care plan (entire Celery task)',
    buckets=[1, 5, 10, 20, 30, 45, 60, 90, 120],
)

llm_call_duration_seconds = Histogram(
    'llm_call_duration_seconds',
    'Duration of the LLM API call specifically',
    buckets=[1, 5, 10, 15, 20, 30, 45, 60],
)

celery_task_duration_seconds = Histogram(
    'celery_task_duration_seconds',
    'Celery task execution duration',
    ['task_name'],
    buckets=[1, 5, 10, 20, 30, 45, 60, 90, 120],
)

# ── Error Metrics ─────────────────────────────────────────

http_request_errors_total = Counter(
    'http_request_errors_total',
    'Total HTTP error responses',
    ['method', 'endpoint', 'status_code'],
)

celery_task_retries_total = Counter(
    'celery_task_retries_total',
    'Celery task retry count',
    ['task_name'],
)

celery_task_failures_total = Counter(
    'celery_task_failures_total',
    'Celery tasks that permanently failed',
    ['task_name'],
)

llm_call_errors_total = Counter(
    'llm_call_errors_total',
    'LLM API call errors',
    ['error_type'],
)
