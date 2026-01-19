# Sales Analytics API

API REST construída com **FastAPI** para gerenciamento de produtos e usuários.  
Possui autenticação **JWT**, filtros, paginação e deploy via **Docker** no **Render**.

---

## Tecnologias

- Python 3.11  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Docker / Docker Compose  
- JWT (autenticação)  
- Render (deploy)

---

## Funcionalidades

- Cadastro de usuários  
- Login com JWT  
- CRUD de produtos  
- Filtragem e paginação de produtos  
- Visualização apenas dos produtos do usuário logado  

---

## Rotas principais

### Usuários

- `POST /users` – Cria usuário  
- `GET /users` – Lista todos os usuários  
- `POST /login` – Login, retorna token JWT  
- `GET /me` – Retorna dados do usuário logado

### Produtos

- `POST /products` – Cria produto (usuário logado)  
- `GET /products` – Lista produtos, com filtros e paginação  
- `GET /my-products` – Lista produtos do usuário logado  
- `PUT /products/{id}` – Atualiza produto (somente dono)  
- `DELETE /products/{id}` – Deleta produto (somente dono)

---

## Variáveis de Ambiente

- `DATABASE_URL` – URL do PostgreSQL (ex.: `postgresql://usuario:senha@host:porta/dbname`)

---

## Rodando localmente com Docker

1. Clone o repositório:  
   ```bash
   git clone https://github.com/larryzmb/sales-analytics-api.git
   cd sales-analytics-api

2. Crie o arquivo .env com sua DATABASE_URL (se necessário)

3. Build e up com Docker Compose:
docker-compose up --build

4. Acesse a API:
http://localhost:8000

5. Documentação interativa (Swagger UI):

http://localhost:8000/docs



Deploy

Deploy realizado no Render usando Docker.
URL da API: https://sales-analytics-api-cw3j.onrender.com



Observações

Todos os endpoints que modificam dados exigem autenticação JWT

Filtragem, ordenação e paginação disponíveis em /products e /my-products

O projeto foi feito como estudo e portfólio