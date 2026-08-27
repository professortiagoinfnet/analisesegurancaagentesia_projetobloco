from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel


from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

### SETUP ###

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token_jwt")

USUARIO_FAKE = {"username": "admin","password": "admin"}
TOKEN_FAKE = "token-fake-admin"
SECRET_KEY = "CHAVE SECRETA"

### DADOS ####
produtos = [
    {
        "id": 1,
        "nome": "Notebook",
        "preco": 3500.0,
        "categoria": "Eletrônico"
    },
    {
        "id": 2,
        "nome": "Mouse",
        "preco": 100.0,
        "categoria": "Eletronico"
    },
    {
        "id": 3,
        "nome": "Teclado",
        "preco": 300.0,
        "categoria": "Eletronico"
    }
]

### FUNÇÕES ###
def validar_token(token: str = Depends(oauth2_scheme)):

    if token != TOKEN_FAKE:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return token

def gerar_token(username: str):

    expiracao = datetime.now(timezone.utc) + timedelta(minutes=30)

    dados = {
        "sub": username,
        "exp": expiracao
    }

    token = jwt.encode(
        dados,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token

def validar_token_jwt(token: str = Depends(oauth2_scheme)):

    erro = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:

        payload = jwt.decode(
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

##### MODELOS #####
class Produto(BaseModel):
    nome: str = Field(min_length=2)
    preco: float = Field(gt=0)
    categoria: str
    descricao: str | None = None
    disponivel : bool = True

#### ROTAS #####
@app.get("/")
def home():
    return {"mensagem": "Minha primeira API com FastAPI"}

@app.get("/produtos")
def listar_produtos():
    return produtos

@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int):

    for produto in produtos:
        if produto["id"] == produto_id:
            return produto

    raise HTTPException(
        status_code=404,
        detail="Produto não encontrado"
    )

@app.get("/listar_produtos_limite")
def listar_produtos(limite: int = 10):
    return produtos[:limite]

@app.post("/produtos", status_code=201)
async def criar_produto(request: Request):

    produto = await request.json()

    novo_produto = {
        "id": len(produtos) + 1,
        "nome": produto["nome"],
        "preco": produto["preco"]
    }
    produtos.append(novo_produto)

    return novo_produto

@app.post("/produtos_pydantic", status_code=201)
def criar_produto(produto: Produto):

    novo_produto = {
        "id": len(produtos) + 1,
        "nome": produto.nome,
        "preco": produto.preco,
        "categoria": produto.categoria
    }

    produtos.append(novo_produto)

    return novo_produto

@app.get("/listar_produtos_limite_protegido")
def listar_produtos(limite: int = 10, token: str = Depends(validar_token_jwt)):
    return produtos[:limite]

@app.post("/token_jwt")
def login(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm )):

    if (
        form_data.username != USUARIO_FAKE["username"]
        or form_data.password != USUARIO_FAKE["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos"
        )

    token = gerar_token(form_data.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

