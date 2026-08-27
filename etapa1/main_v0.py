from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

class Produto(BaseModel):
    nome: str = Field(min_length=2)
    preco: float = Field(gt=0)
    categoria: str
    descricao: str | None = None
    disponivel : bool = True


# produto_teste = Produto(nome="Tablet", preco=6500.0)
# print(f"produto_teste     :{produto_teste}, {produto_teste.nome}, {produto_teste.preco}")
# print(f"produto_teste_dict:{produto_teste.model_dump()}")

app = FastAPI()

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

print(produtos)

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



