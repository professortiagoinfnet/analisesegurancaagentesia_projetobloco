from fastapi import FastAPI
from sqlmodel import SQLModel

from database import engine
from routes.auth_route import router as auth_router
from routes.prediction_route import router as prediction_router

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(auth_router)
app.include_router(prediction_router)