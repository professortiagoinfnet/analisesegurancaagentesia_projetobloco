from pydantic import BaseModel, ConfigDict

class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str