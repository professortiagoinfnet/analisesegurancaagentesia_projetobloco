import time

from fastapi import FastAPI, Request
from sqlmodel import SQLModel

from database import engine
from routes.auth_route import router as auth_router
from routes.prediction_route import router as prediction_router

app = FastAPI()

@app.middleware("http")
async def process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    final = time.time()
    response.headers["X-Process-Time"] = str(final - start)
    return response



SQLModel.metadata.create_all(engine)

app.include_router(auth_router)
app.include_router(prediction_router)