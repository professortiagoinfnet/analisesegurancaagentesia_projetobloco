from pydantic import BaseModel

class PredictionResponse(BaseModel):
    message: str
    intent: str

class PredictionValid(BaseModel):
    message: str
    valid: str