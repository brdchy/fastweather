from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from commands import *

weather_data1 = None
weather_data2 = None

async def fetch_weather_data():
    global weather_data1, weather_data2
    try:
        weather_data1 = await get_weather_wttr()
    except Exception as e:
        print(f"Error fetching weather data from source 1: {e}")
        asyncio.create_task(retry_fetch_weather_data1())
    try:
        weather_data2 = await get_weather_weatherapi()
    except Exception as e:
        print(f"Error fetching weather data from source 2: {e}")
        asyncio.create_task(retry_fetch_weather_data2())

async def retry_fetch_weather_data1():
    await asyncio.sleep(900) 
    try:
        global weather_data1
        weather_data1 = await get_weather_wttr()
    except Exception as e:
        print(f"Retry error fetching weather data from source 1: {e}")
        asyncio.create_task(retry_fetch_weather_data1())

async def retry_fetch_weather_data2():
    await asyncio.sleep(900)
    try:
        global weather_data2
        weather_data2 = await get_weather_weatherapi()
    except Exception as e:
        print(f"Retry error fetching weather data from source 2: {e}")
        asyncio.create_task(retry_fetch_weather_data2())

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_weather_data, 'interval', hours=6)
    scheduler.start()
    await fetch_weather_data()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/forecast")
async def weather():
    if weather_data1 and weather_data2:
        return {"weather_data1": weather_data1, "weather_data2": weather_data2}
    elif weather_data1:
        return {"weather_data1": weather_data1}
    elif weather_data2:
        return {"weather_data2": weather_data2}
    else:
        raise HTTPException(status_code=503, detail="Не удалось получить данные о погоде")
    
@app.get("/weather")
async def weather():
    current_weather_data1 = get_current_weather_wttr()
    current_weather_data2 = get_current_weather_weatherapi()
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
    uvicorn.run(app, host="192.168.0.7", port=6565)