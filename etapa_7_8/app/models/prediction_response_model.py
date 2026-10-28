from pydantic import BaseModel

class PredictionResponse(BaseModel):
    message: str
    intent: str
    probability: float

class PredictionValid(BaseModel):
    message: str
    valid: str