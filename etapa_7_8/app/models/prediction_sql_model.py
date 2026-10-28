from sqlmodel import SQLModel, Field

class Prediction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    intent: str
    owner_id: int = Field(foreign_key="user.id")