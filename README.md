# Projeto de Bloco — Análise e Segurança de Agentes de IA

Projeto didático desenvolvido para a disciplina **Projeto de Bloco**, do bloco **Análise e Segurança de Agentes de IA**.

O repositório apresenta, de forma incremental, a construção de uma API com **FastAPI**, passando por conceitos básicos de desenvolvimento de APIs até mecanismos de autenticação, persistência de dados e controle de acesso.

O objetivo é utilizar uma aplicação simples como base para discutir conceitos relacionados à construção e à segurança de sistemas e APIs que podem fazer parte de soluções envolvendo agentes de IA.

## Objetivos do projeto

O projeto permite exercitar conceitos como:

* criação de APIs REST com FastAPI;
* definição e validação de dados com Pydantic;
* parâmetros de rota e de consulta;
* tratamento de erros HTTP;
* autenticação baseada em OAuth2 e Bearer Token;
* criação e validação de tokens JWT;
* persistência de dados com SQLite;
* mapeamento de tabelas com SQLModel;
* consultas ao banco de dados com SQLModel;
* injeção de dependências com FastAPI;
* identificação do usuário autenticado;
* autorização e controle de acesso a recursos;
* mitigação de falhas de autorização como **BOLA (Broken Object Level Authorization)**;
* rejeição de campos adicionais em modelos de entrada com `extra="forbid"`.

## Estrutura do projeto

```text
local/
├── etapa1/
│   ├── main_v0.py
│   ├── main_v1.py
│   ├── main_v2_jwt.py
│   ├── test.py
│   └── test_v0.py
│
└── etapa2/
    ├── main.py
    ├── database.py
    ├── create_database.py
    ├── populate_database.py
    │
    ├── models/
    │   ├── prediction_request_model.py
    │   ├── prediction_response_model.py
    │   ├── prediction_sql_model.py
    │   └── user_sql_model.py
    │
    ├── routes/
    │   ├── auth_route.py
    │   └── prediction_route.py
    │
    └── security/
        ├── dependencies.py
        └── jwt.py
```

## Etapa 1 — Fundamentos de FastAPI e autenticação

A primeira etapa apresenta uma evolução progressiva da API.

### `main_v0.py`

Versão inicial utilizada para apresentar fundamentos do FastAPI:

* criação da aplicação;
* rotas `GET` e `POST`;
* path parameters;
* query parameters;
* códigos de status HTTP;
* tratamento de erros com `HTTPException`;
* recebimento de JSON diretamente pela requisição;
* validação de entrada utilizando Pydantic.

A aplicação utiliza uma lista em memória para armazenar produtos.

### `main_v1.py`

Adiciona autenticação simples utilizando:

* `OAuth2PasswordBearer`;
* `OAuth2PasswordRequestForm`;
* Bearer Token;
* rotas protegidas com `Depends`.

Nesta versão é utilizado um token fixo apenas para demonstrar o funcionamento da autenticação.

### `main_v2_jwt.py`

Substitui o token fixo por um **JSON Web Token (JWT)**.

O token contém:

* `sub`: identificação do usuário;
* `exp`: data de expiração do token.

O JWT é assinado utilizando o algoritmo `HS256` e possui validade de 30 minutos.

## Etapa 2 — Banco de dados, JWT e autorização

A segunda etapa organiza a aplicação em módulos e adiciona persistência com **SQLite** e **SQLModel**.

### Banco de dados

O arquivo `database.py` cria o engine do SQLModel e disponibiliza uma sessão por meio da dependência `get_session()`.

São utilizadas duas entidades principais:

### User

```text
id
username
password
```

### Prediction

```text
id
text
intent
owner_id
```

O campo `owner_id` relaciona uma prediction ao usuário proprietário do recurso.

## Autenticação JWT

O endpoint:

```http
POST /token
```

recebe `username` e `password` por meio de `OAuth2PasswordRequestForm`.

Quando as credenciais são válidas, a API retorna um token JWT:

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

O módulo `security/jwt.py` é responsável por:

* gerar o token;
* definir sua expiração;
* validar sua assinatura;
* recuperar o usuário armazenado no campo `sub`;
* rejeitar tokens inválidos ou expirados.

## Usuário autenticado

A função `get_current_user()`, localizada em `security/dependencies.py`, utiliza o JWT recebido na requisição para identificar o usuário correspondente no banco de dados.

Essa dependência pode ser utilizada pelas rotas que precisam conhecer o usuário autenticado.

## Controle de acesso e BOLA

A rota:

```http
GET /predictions/{prediction_id}
```

não procura uma prediction apenas pelo seu identificador.

A consulta também verifica se o recurso pertence ao usuário autenticado:

```python
statement = select(Prediction).where(
    Prediction.id == prediction_id,
    Prediction.owner_id == current_user.id
)
```

Dessa forma, conhecer ou alterar o ID na URL não é suficiente para acessar um recurso pertencente a outro usuário.

Esse controle está relacionado à prevenção de **Broken Object Level Authorization (BOLA)**, uma das principais falhas de autorização encontradas em APIs.

## Validação de entrada

O modelo `PredictionRequest` utiliza:

```python
model_config = ConfigDict(extra="forbid")
```

Com essa configuração, propriedades que não foram declaradas no modelo são rejeitadas durante a validação da requisição.

Exemplo de modelo aceito:

```json
{
  "text": "Quero cancelar minha compra"
}
```

Uma requisição contendo campos adicionais não previstos pelo modelo será rejeitada pelo Pydantic.

## Requisitos

Recomenda-se utilizar **Python 3.10 ou superior**.

Principais dependências utilizadas no projeto:

```text
fastapi
uvicorn
pydantic
sqlmodel
PyJWT
python-multipart
requests
```

As dependências podem ser instaladas com:

```bash
pip install fastapi uvicorn pydantic sqlmodel PyJWT python-multipart requests
```

## Executando a Etapa 1

Entre no diretório:

```bash
cd local/etapa1
```

Para executar a primeira versão:

```bash
uvicorn main_v0:app --reload
```

Para executar a versão com autenticação simples:

```bash
uvicorn main_v1:app --reload
```

Para executar a versão com JWT:

```bash
uvicorn main_v2_jwt:app --reload
```

A documentação interativa estará disponível em:

```text
http://127.0.0.1:8000/docs
```

## Executando a Etapa 2

Entre no diretório:

```bash
cd local/etapa2
```

### 1. Criar o banco de dados

```bash
python create_database.py
```

### 2. Popular o banco com dados de exemplo

```bash
python populate_database.py
```

O script adiciona os usuários de laboratório:

| Usuário | Senha   |
| ------- | ------- |
| `admin` | `admin` |
| `jose`  | `1234`  |

Também são adicionadas predictions associadas aos respectivos usuários.

### 3. Iniciar a API

```bash
uvicorn main:app --reload
```

### 4. Abrir o Swagger

Acesse:

```text
http://127.0.0.1:8000/docs
```

## Testando a autenticação

No Swagger, execute primeiro:

```http
POST /token
```

utilizando, por exemplo:

```text
username: admin
password: admin
```

Copie o token retornado ou utilize o botão **Authorize** do Swagger para autenticar as próximas requisições.

Em seguida, teste:

```http
GET /predictions/{prediction_id}
```

O resultado dependerá do usuário autenticado e do proprietário da prediction solicitada.

## Exemplos de dados

O banco de laboratório é populado inicialmente com os seguintes exemplos:

| ID | Texto                       | Intent       | Proprietário |
| -: | --------------------------- | ------------ | ------------ |
|  1 | Meu pedido não chegou       | reclamacao   | admin        |
|  2 | Quero cancelar minha compra | cancelamento | admin        |
|  3 | Qual o prazo de entrega?    | informacao   | jose         |

Isso permite demonstrar que usuários diferentes não devem ter acesso irrestrito aos recursos uns dos outros.

## Conceitos de segurança abordados

### Autenticação

Verificação da identidade do usuário antes de permitir acesso a recursos protegidos.

### Autorização

Verificação das operações e dos recursos que um usuário autenticado pode acessar.

### JWT

Uso de tokens assinados e com tempo de expiração para representar uma sessão autenticada.

### BOLA

Verificação do proprietário do objeto antes de retornar um recurso solicitado por ID.

### Validação de entrada

Uso do Pydantic para definir explicitamente os campos aceitos pela API e rejeitar dados inesperados.

### Consultas com SQLModel

Uso da API de consultas do SQLModel, evitando a construção de comandos SQL a partir de dados fornecidos diretamente pelo usuário nas rotas da aplicação.

## Observações de segurança

> **Importante:** este projeto possui finalidade exclusivamente didática.

Para facilitar os exercícios em sala de aula, existem simplificações que **não devem ser utilizadas em produção**, como:

* senhas armazenadas em texto puro;
* usuários e senhas de exemplo conhecidos;
* chave JWT escrita diretamente no código;
* ausência de gerenciamento seguro de secrets;
* configurações simplificadas de autenticação e autorização.

Em uma aplicação real, recomenda-se, entre outras medidas:

* armazenar hashes de senha utilizando algoritmo apropriado;
* manter chaves e secrets em variáveis de ambiente ou serviço de gerenciamento de secrets;
* utilizar uma chave JWT forte;
* implementar políticas adequadas de autorização;
* adicionar testes automatizados de segurança;
* aplicar controles adicionais recomendados pelo OWASP para APIs.

## Tecnologias utilizadas

* Python
* FastAPI
* Pydantic
* SQLModel
* SQLite
* OAuth2
* JWT
* Uvicorn

## Finalidade acadêmica

Este repositório foi criado como material de apoio para aulas e exercícios da disciplina **Projeto de Bloco**, pertencente ao bloco **Análise e Segurança de Agentes de IA**.

O código prioriza simplicidade e clareza didática, permitindo acompanhar a evolução de uma API desde sua implementação básica até a introdução de controles de autenticação, autorização e segurança.
