from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from models.prediction_request_model import PredictionRequest
from models.prediction_response_model import PredictionResponse, PredictionValid
from fastapi import Response
import time

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.prediction_sql_model import Prediction
from models.user_sql_model import User
from security.dependencies import get_current_user

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/predictions/{prediction_id}")
def get_prediction(
    prediction_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Prediction).where(
        Prediction.id == prediction_id,
        Prediction.owner_id == current_user.id
    )

    prediction = session.exec(statement).first()

    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction não encontrada")

    return prediction

@router.get("/predicitons_limited")
@limiter.limit("5/minute")
def get_all_predicitons(
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    if current_user.id != 1:
        raise HTTPException(status_code=404, detail="Prediction não encontrada")
    
    statement = select(Prediction).where(
        Prediction.owner_id > 0
    )

    predictions = session.exec(statement).fetchall()

    if len(predictions) == 0:
        raise HTTPException(status_code=404, detail="Prediction não encontrada")
    
    return predictions

@router.get("/predicitons")
def get_all_predicitons(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    if current_user.id != 1:
        raise HTTPException(status_code=404, detail="Prediction não encontrada")
    
    statement = select(Prediction).where(
        Prediction.owner_id > 0
    )

    predictions = session.exec(statement).fetchall()

    if len(predictions) == 0:
        raise HTTPException(status_code=404, detail="Prediction não encontrada")
    
    return predictions

@router.post("/predict")
def predict (predictionRequest: PredictionRequest, response: Response):
    predictionResponse = PredictionResponse(
        message=predictionRequest.message,
        intent='cancelamento'
    )
    return predictionResponse

@router.post("/valid")
def valid(predictionRequest: PredictionRequest, response: Response):
    predictionResponse = PredictionValid(
        message=predictionRequest.message,
        valid='Válido' if len(predictionRequest.message) > 5 else "Inválido"
    )
    return predictionResponse

                               
