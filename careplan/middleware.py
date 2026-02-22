from django.http import JsonResponse

from .exceptions import BaseAppException, BlockError, WarningException
from .metrics import careplan_requests_total, careplan_duplicate_blocks_total


class ExceptionHandlerMiddleware:
    """
    Catches all BaseAppException and converts them to uniform JSON responses.

    Before:  every view does isinstance() checks and builds JsonResponse manually
    After:   services raise exceptions, this middleware catches ALL of them in ONE place
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # Only handle our custom exceptions
        if isinstance(exception, BaseAppException):
            if isinstance(exception, BlockError):
                careplan_requests_total.labels(status='blocked').inc()
                careplan_duplicate_blocks_total.labels(reason=exception.code).inc()
            elif isinstance(exception, WarningException):
                careplan_requests_total.labels(status='warning').inc()

            return JsonResponse(
                exception.to_dict(),
                status=exception.http_status,
            )

        # Return None = let Django handle it (500 error page, etc.)
        return None
