import time

from .metrics import http_request_duration_seconds, http_request_errors_total


class PrometheusMetricsMiddleware:
    """Records request duration and error counts for every HTTP request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        duration = time.monotonic() - start

        endpoint = self._normalize_path(request.path)
        method = request.method
        status_code = str(response.status_code)

        http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint,
            status_code=status_code,
        ).observe(duration)

        if response.status_code >= 400:
            http_request_errors_total.labels(
                method=method,
                endpoint=endpoint,
                status_code=status_code,
            ).inc()

        return response

    @staticmethod
    def _normalize_path(path):
        """Replace numeric IDs with {id} to prevent label cardinality explosion."""
        parts = path.strip('/').split('/')
        normalized = []
        for part in parts:
            if part.isdigit():
                normalized.append('{id}')
            else:
                normalized.append(part)
        return '/' + '/'.join(normalized) + '/' if normalized else '/'
