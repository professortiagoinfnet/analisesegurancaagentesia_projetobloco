from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from database import engine
from routes.auth_route import router as auth_router
from routes.prediction_route import router as prediction_router

app = FastAPI()

SQLModel.metadata.create_all(engine)


origens_permitidas = [
    "http://localhost:3000",
    "http://localhost:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    # response.headers["Content-Security-Policy"] = "default-src 'self'"

    return response

app.include_router(auth_router)
app.include_router(prediction_router)