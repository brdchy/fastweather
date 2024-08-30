from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from database import Base

class WeatherLookups(Base):
    __tablename__ = "weather_lookups"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    date_time = Column(DateTime)
    temperature = Column(Float)
    feels_like = Column(Float)
    description = Column(Text)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    pressure = Column(Float)
    precipitation = Column(Float)
    uv_index = Column(Float, nullable=True)
    source = Column(String)

class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    date_time = Column(DateTime)
    temperature = Column(Float)
    feels_like = Column(Float)
    description = Column(Text)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    pressure = Column(Float)
    precipitation = Column(Float)
    uv_index = Column(Float, nullable=True)
    source = Column(String)    