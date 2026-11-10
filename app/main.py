from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlmodel import Session, select

from app.database import create_db_and_tables, get_session
from app.models import ServiceCreate, ServiceRead, ServiceDB

from uuid import UUID
from fastapi import HTTPException
from app.models import HealthCheckDB, HealthCheckRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="CloudOps API",
    description="Cloud service monitoring and incident management",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "cloudops-api",
    }


@app.post(
    "/services",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    service: ServiceCreate,
    session: Session = Depends(get_session),
):
    db_service = ServiceDB(
        name=service.name,
        health_url=str(service.health_url),
    )

    session.add(db_service)
    session.commit()
    session.refresh(db_service)

    return db_service


@app.get("/services", response_model=list[ServiceRead])
def list_services(
    session: Session = Depends(get_session),
):
    return session.exec(select(ServiceDB)).all()


@app.get(
    "/services/{service_id}/checks",
    response_model=list[HealthCheckRead],
)
def list_health_checks(
    service_id: UUID,
    session: Session = Depends(get_session),
):
    service = session.get(ServiceDB, service_id)

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    statement = (
        select(HealthCheckDB)
        .where(HealthCheckDB.service_id == service_id)
        .order_by(HealthCheckDB.checked_at.desc())
        .limit(100)
    )

    return session.exec(statement).all()
