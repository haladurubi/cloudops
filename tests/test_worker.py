
from sqlmodel import Session, select

from app.models import ServiceDB, HealthCheckDB
from app.monitoring import HealthResult
from app.worker import run_checks, LOCAL_HEALTH_URL


def test_worker_saves_health_result(test_engine):
    with Session(test_engine) as session:
        service = ServiceDB(
            name="Local API",
            health_url=LOCAL_HEALTH_URL,
        )

        session.add(service)
        session.commit()
        session.refresh(service)

        def fake_checker(url):
            return HealthResult(
                status="healthy",
                http_status=200,
                response_time_ms=12.5,
            )

        count = run_checks(
            session,
            checker=fake_checker,
        )

        records = session.exec(
            select(HealthCheckDB)
        ).all()

        assert count == 1
        assert len(records) == 1
        assert records[0].service_id == service.id
        assert records[0].status == "healthy"


def test_worker_skips_unapproved_urls(test_engine):
    with Session(test_engine) as session:
        service = ServiceDB(
            name="External API",
            health_url="https://example.com/health",
        )

        session.add(service)
        session.commit()

        def forbidden_checker(url):
            raise AssertionError(
                "Worker attempted an unapproved request"
            )

        count = run_checks(
            session,
            checker=forbidden_checker,
        )

        assert count == 0


def test_worker_records_failure(test_engine):
    with Session(test_engine) as session:
        service = ServiceDB(
            name="Local API",
            health_url=LOCAL_HEALTH_URL,
        )

        session.add(service)
        session.commit()

        def fake_failure(url):
            return HealthResult(
                status="unhealthy",
                http_status=None,
                response_time_ms=5.0,
                error="ConnectError",
            )

        run_checks(
            session,
            checker=fake_failure,
        )

        record = session.exec(
            select(HealthCheckDB)
        ).first()

        assert record is not None
        assert record.status == "unhealthy"
        assert record.error == "ConnectError"
