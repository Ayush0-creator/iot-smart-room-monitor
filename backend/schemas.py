from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SensorReadingCreate(BaseModel):
    device_id: str = Field(..., min_length=2, max_length=50)
    temperature: float = Field(..., ge=-50, le=100)
    humidity: float = Field(..., ge=0, le=100)


class SensorReadingResponse(BaseModel):
    id: int
    device_id: str
    temperature: float
    humidity: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
