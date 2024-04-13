import sys
sys.path.append(".")
import logging

import uvicorn
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ordermgmt.routers import customers, restaurant, internal

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler(timezone='utc')
    scheduler.start()
    app.scheduler = scheduler
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(customers.router)
app.include_router(restaurant.router)
app.include_router(internal.router)


@app.get("/", tags=["docs"])
async def root():
    return RedirectResponse(url='/docs')


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
