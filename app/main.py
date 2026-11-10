from fastapi import FastAPI

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
