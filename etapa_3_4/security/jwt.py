from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode, InvalidTokenError

SECRET_KEY = "minha-chave-secreta"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def gerar_token(username: str):
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=30)

    dados = {
        "sub": username,
        "exp": expiracao
    }

    return encode(
        dados,
        SECRET_KEY,
        algorithm="HS256"
    )


def validar_token(
    token: str = Depends(oauth2_scheme)
):
    erro = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        username = payload.get("sub")

        if username is None:
            raise erro

    except InvalidTokenError:
        raise erro

    return username