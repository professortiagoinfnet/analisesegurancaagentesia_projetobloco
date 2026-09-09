from pydantic import BaseModel

class PredictionResponse(BaseModel):
    id: int
    text: str
    intent: str