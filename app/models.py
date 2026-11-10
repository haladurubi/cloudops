from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class ServiceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    health_url: HttpUrl


class ServiceRead(ServiceCreate):
    id: UUID
