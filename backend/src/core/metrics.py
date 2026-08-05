from threading import Lock


class MetricsCollector:
    def __init__(self) -> None:
        self._lock = Lock()
        self._total_requests = 0
        self._requests_by_status: dict[str, int] = {}
        self._total_errors = 0
        self._total_response_time_ms = 0.0

    def record(self, status_code: int, elapsed_ms: float) -> None:
        status = str(status_code)
        with self._lock:
            self._total_requests += 1
            self._requests_by_status[status] = (
                self._requests_by_status.get(status, 0) + 1
            )
            if status_code >= 500:
                self._total_errors += 1
            self._total_response_time_ms += max(elapsed_ms, 0.0)

    def snapshot(self) -> dict[str, int | float | dict[str, int]]:
        with self._lock:
            average = (
                self._total_response_time_ms / self._total_requests
                if self._total_requests
                else 0.0
            )
            return {
                "total_requests": self._total_requests,
                "requests_by_status": dict(self._requests_by_status),
                "total_errors": self._total_errors,
                "average_response_time_ms": average,
            }

    def reset(self) -> None:
        with self._lock:
            self._total_requests = 0
            self._requests_by_status.clear()
            self._total_errors = 0
            self._total_response_time_ms = 0.0


metrics_collector = MetricsCollector()
