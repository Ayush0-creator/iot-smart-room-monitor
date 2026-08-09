from fastapi import FastAPI
from database import Base, engine
from routes.sensors import router as sensor_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IoT Smart Room Monitor API",
    description="REST API for collecting and monitoring IoT sensor data.",
    version="1.0.0"
)

app.include_router(sensor_router)


@app.get("/")
def root():
    return {
        "project": "IoT Smart Room Monitor",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
