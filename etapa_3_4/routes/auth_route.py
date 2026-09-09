from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from database import get_session
from models.user_sql_model import User
from security.jwt import gerar_token


router = APIRouter()


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    statement = select(User).where(
        User.username == form_data.username
    )

    user = session.exec(statement).first()

    if user is None or user.password != form_data.password:
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos"
        )

    token = gerar_token(user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }