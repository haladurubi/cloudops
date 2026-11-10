
from uuid import UUID

from sqlmodel import Session

from app.models import ServiceDB, HealthCheckDB
from app.monitoring import HealthResult


def save_health_result(
    session: Session,
    service_id: UUID,
    result: HealthResult,
) -> HealthCheckDB:

    service = session.get(ServiceDB, service_id)

    if service is None:
        raise ValueError("Service does not exist")

    record = HealthCheckDB(
        service_id=service_id,
        status=result.status,
        http_status=result.http_status,
        response_time_ms=result.response_time_ms,
        error=result.error,
    )

    session.add(record)
    session.commit()
    session.refresh(record)

    return record
