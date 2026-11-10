from fastapi import FastAPI

from uuid import uuid4

from fastapi import status

from app.models import ServiceCreate, ServiceRead

app = FastAPI(
    title="CloudOps API",
    description="Cloud service monitoring and incident management",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "cloudops-api"
    }


services: dict[str, ServiceRead] = {}


@app.post(
    "/services",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
)

def create_service(service: ServiceCreate):
    new_service = ServiceRead(
        id=uuid4(),
        **service.model_dump()
    )

    services[str(new_service.id)] = new_service

    return new_service


@app.get("/services", response_model=list[ServiceRead])
def list_services():
    return list(services.values())

