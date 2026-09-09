import requests

dados = {
    "nome": "Smartphone",
    "preco": "teste"
}

dados2 = {
    "username": "admin",
    "password": "admin"
}

url_listar_produtos_limite  = "http://127.0.0.1:8000/listar_produtos_limite?limite=10"
url_criar_produto           = "http://127.0.0.1:8000/produtos"
response = requests.get(url_listar_produtos_limite)
print(response.json())
response = requests.post(url_criar_produto, json=dados)
print(response.json())
response = requests.get(url_listar_produtos_limite)
print(response.json())

response = requests.post("http://127.0.0.1:8000/token", dados2)
print(response.json())

