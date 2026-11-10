from uuid import UUID, uuid4
from pydantic import BaseModel, Field, HttpUrl
from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime, timezone



class ServiceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    health_url: HttpUrl


class ServiceRead(ServiceCreate):
    id: UUID

class ServiceDB(SQLModel, table=True):
    __tablename__ = "services"

    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    name: str
    health_url: str


class HealthCheckDB(SQLModel, table=True):
    __tablename__ = "health_checks"

    id: UUID = SQLField(
        default_factory=uuid4,
        primary_key=True,
    )

    service_id: UUID = SQLField(
        foreign_key="services.id",
        index=True,
    )

    checked_at: datetime = SQLField(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    status: str
    http_status: int | None = None
    response_time_ms: float
    error: str | None = None


class HealthCheckRead(BaseModel):
    id: UUID
    service_id: UUID
    checked_at: datetime
    status: str
    http_status: int | None
    response_time_ms: float
    error: str | None
