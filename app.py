from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from commands import *
from commands import get_current_weather_wttr, get_current_weather_weatherapi
from database import SessionLocal, engine
from models import Base, WeatherLookups

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def save_weather_data_to_db():
    db = next(get_db())
    weather_data1 = get_current_weather_wttr()
    weather_data2 = get_current_weather_weatherapi()
    if weather_data1:
        db_weather1 = WeatherLookups(**weather_data1)
        db.add(db_weather1)
    if weather_data2:
        db_weather2 = WeatherLookups(**weather_data2)
        db.add(db_weather2)
    db.commit()
    
weather_data1 = None
weather_data2 = None

async def fetch_weather_data():
    global weather_data1, weather_data2
    try:
        weather_data1 = await asyncio.to_thread(get_weather_wttr)
    except Exception as e:
        print(f"Error fetching weather data from source 1: {e}")
        asyncio.create_task(retry_fetch_weather_data1())
    try:
        weather_data2 = await asyncio.to_thread(get_weather_weatherapi)
    except Exception as e:
        print(f"Error fetching weather data from source 2: {e}")
        asyncio.create_task(retry_fetch_weather_data2())

async def retry_fetch_weather_data1():
    await asyncio.sleep(900) 
    try:
        global weather_data1
        weather_data1 = await asyncio.to_thread(get_weather_wttr)
    except Exception as e:
        print(f"Retry error fetching weather data from source 1: {e}")
        asyncio.create_task(retry_fetch_weather_data1())

async def retry_fetch_weather_data2():
    await asyncio.sleep(900)
    try:
        global weather_data2
        weather_data2 = await asyncio.to_thread(get_weather_weatherapi)
    except Exception as e:
        print(f"Retry error fetching weather data from source 2: {e}")
        asyncio.create_task(retry_fetch_weather_data2())

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_weather_data, 'interval', hours=6)
    scheduler.add_job(save_weather_data_to_db, 'interval', hours=1)
    scheduler.start()
    await fetch_weather_data()
    await save_weather_data_to_db()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/forecast")
async def forecast():
    if weather_data1 and weather_data2:
        return {"weather_data1": weather_data1, "weather_data2": weather_data2}
    elif weather_data1:
        return {"weather_data1": weather_data1}
    elif weather_data2:
        return {"weather_data2": weather_data2}
    else:
        raise HTTPException(status_code=503, detail="Не удалось получить данные о погоде")
    
@app.get("/weather")
async def current_weather():
    current_weather_data1 = await asyncio.to_thread(get_current_weather_wttr)
    current_weather_data2 = await asyncio.to_thread(get_current_weather_weatherapi)
    if current_weather_data1 and current_weather_data2:
        return {"weather_data1": current_weather_data1, "weather_data2": current_weather_data2}
    elif current_weather_data1:
        return {"weather_data1": current_weather_data1}
    elif current_weather_data2:
        return {"weather_data2": current_weather_data2}
    else:
        raise HTTPException(status_code=503, detail="Не удалось получить данные о погоде")    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.61.36.12", port=6565)