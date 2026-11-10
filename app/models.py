from uuid import UUID, uuid4
from pydantic import BaseModel, Field, HttpUrl
from sqlmodel import SQLModel, Field as SQLField



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