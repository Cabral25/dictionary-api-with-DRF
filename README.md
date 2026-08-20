# dictionary-api-with-DRF

API REST para gerenciamento de palavras e seus respectivos significados, desenvolvida com Django REST Framework e PostgreSQL.

## Sobre o projeto

O projeto foi desenvolvido com o objetivo de praticar a construção de APIs REST, integração com banco de dados, autenticação, serialização de dados, versionamento e utilização de Docker.

## Funcionalidades

🔹 Cadastro de palavras
🔹 Consulta de palavras
🔹 Consulta de uma palavra específica
🔹 Atualização de palavras
🔹 Exclusão de palavras
🔹 Cadastro e gerenciamento de significados
🔹 Relacionamento entre palavras e significados
🔹 Validação dos dados através de serializers
🔹 Persistência dos dados em PostgreSQL

## Tecnologias utilizadas

🔹 Python
🔹 Django
🔹 Django REST Framework
🔹 Django Test Framework
🔹 PostgreSQL
🔹 Docker
🔹 Docker Compose

## Como executar

Pré-requisitos:
🔹 Docker
🔹 Docker compose

1. Clone o repositório
git clone https://github.com/Cabral25/dictionary-api-with-DRF
cd dictionary_api

2. Configure as variáveis de ambiente

Crie um arquivo .env na raiz do projeto:

POSTGRES_DB=dictionary_api_with_drf
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha 
DB_NAME=dictionary_api_with_drf
DB_USER=postgres 
DB_PASSWORD=sua_senha 
DB_HOST=db 
DB_PORT=5432

3. Suba os containers
docker compose up -d

4. Execute as migrações
docker compose exec web python manage.py migrate

5. Acesse a API

A API estará disponível em:

http://localhost:8000/

## Endpoints

Método	   Endpoint	                               Descrição
GET/POST   /api/api-version/words/	               Lista e cria as palavras
GET        /api/api-version/words/search/          Busca uma palavra
GET	       /api/api-version/words/{word}/	       Mostra uma palavra em detalhes
PUT	       /api/api-version/words/update/{word}/   Atualiza uma palavra
DELETE	   /api/api-version/words/delete/{word}/   Remove uma palavra
POST       /api/users/register/
POST       /api/api-version/login                  Realiza o login
POST       /api/api-version/logout                 Permite realizar o logout

## Exemplos de requisição

Criar uma palavra

POST /api/v1/words/
Content-Type: application/json

Resposta
{
    "word": "backend",
    "meaning": "Field of software development that handles the logic"
}

## Banco de dados

O projeto utiliza PostgreSQL como banco de dados.
O PostgreSQL é executado em um container separado e os dados são persistidos através de um volume Docker.

## Testes

Os testes da API foram desenvolvidos utilizando o framework de testes do Django e o 'APITestCase' fornecido pelo Django REST Framework.
Para executar os testes:

```bash
docker compose exec web python manage.py test
```

## Docker

### O projeto utiliza Docker Compose para executar:

    🔹 aplicação Django
    🔹 banco de dados PostgreSQL

A comunicação entre os containers é realizada através da rede criada pelo Docker Compose.

## O que aprendi

Durante o desenvolvimento, pratiquei a construção de APIs REST com Django REST Framework, relacionamento entre modelos, serialização e validação de dados, integração com PostgreSQL, containerização da aplicação com Docker e execução de testes automatizados.