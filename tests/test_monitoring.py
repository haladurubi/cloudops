
import httpx

from app.monitoring import check_url


def test_healthy_service():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200)
    )

    result = check_url(
        "https://example.com/health",
        transport=transport,
    )

    assert result.status == "healthy"
    assert result.http_status == 200
    assert result.response_time_ms >= 0


def test_unhealthy_service():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(503)
    )

    result = check_url(
        "https://example.com/health",
        transport=transport,
    )

    assert result.status == "unhealthy"
    assert result.http_status == 503


def test_connection_failure():
    def fail(request):
        raise httpx.ConnectError(
            "Connection refused",
            request=request,
        )

    transport = httpx.MockTransport(fail)

    result = check_url(
        "https://example.com/health",
        transport=transport,
    )

    assert result.status == "unhealthy"
    assert result.http_status is None
    assert result.error == "ConnectError"
