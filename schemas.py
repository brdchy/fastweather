from pydantic import BaseModel
from datetime import datetime

class WeatherLookupsCreate(BaseModel):
    date_time: datetime
    temperature: float
    feels_like: float
    description: str
    humidity: float
    wind_speed: float
    wind_direction: str
    pressure: float
    precipitation: float
    uv_index: float = None
    source: str

class WeatherLookups(WeatherLookupsCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True