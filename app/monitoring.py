
from dataclasses import dataclass
from time import perf_counter

import httpx


@dataclass
class HealthResult:
    status: str
    http_status: int | None
    response_time_ms: float
    error: str | None = None


def check_url(
    url: str,
    *,
    transport: httpx.BaseTransport | None = None,
) -> HealthResult:
    start = perf_counter()

    try:
        with httpx.Client(
            timeout=5.0,
            follow_redirects=False,
            transport=transport,
        ) as client:
            response = client.get(url)

        elapsed = (perf_counter() - start) * 1000

        return HealthResult(
            status=(
                "healthy"
                if 200 <= response.status_code < 300
                else "unhealthy"
            ),
            http_status=response.status_code,
            response_time_ms=round(elapsed, 2),
        )

    except httpx.RequestError as exc:
        elapsed = (perf_counter() - start) * 1000

        return HealthResult(
            status="unhealthy",
            http_status=None,
            response_time_ms=round(elapsed, 2),
            error=type(exc).__name__,
        )
