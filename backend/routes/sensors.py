from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import SensorReading
from schemas import SensorReadingCreate, SensorReadingResponse

router = APIRouter(
    prefix="/api/v1/sensors",
    tags=["Sensors"]
)


@router.post(
    "/readings",
    response_model=SensorReadingResponse,
    status_code=201
)
def create_reading(
    reading: SensorReadingCreate,
    db: Session = Depends(get_db)
):
    sensor_data = SensorReading(
        device_id=reading.device_id,
        temperature=reading.temperature,
        humidity=reading.humidity
    )

    db.add(sensor_data)
    db.commit()
    db.refresh(sensor_data)

    return sensor_data


@router.get(
    "/readings",
    response_model=list[SensorReadingResponse]
)
def get_readings(
    device_id: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    if limit < 1 or limit > 200:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 200"
        )

    query = db.query(SensorReading)

    if device_id:
        query = query.filter(
            SensorReading.device_id == device_id
        )

    return (
        query
        .order_by(SensorReading.created_at.desc())
        .limit(limit)
        .all()
    )
