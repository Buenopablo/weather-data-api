# Weather Data API

API REST desenvolvida em Python com Django REST Framework para coleta, armazenamento e consulta de dados meteorológicos utilizando a API pública da [OpenWeather](https://openweathermap.org/api).

O projeto integra uma fonte externa de dados, processa as informações recebidas e armazena os registros em um banco de dados relacional PostgreSQL, disponibilizando endpoints REST para consulta do histórico meteorológico.

## Objetivo

Desenvolver uma aplicação capaz de:

- Consultar informações meteorológicas de cidades através da API OpenWeather.
- Processar e organizar os dados recebidos.
- Armazenar os registros em um banco de dados PostgreSQL.
- Disponibilizar os dados através de uma API REST.
- Permitir consultas e filtros por cidade.
- Documentar os endpoints utilizando Swagger/OpenAPI.
- Executar a aplicação e o banco de dados em ambiente Docker.

## Tecnologias utilizadas

| Tecnologia            | Finalidade                             |
| --------------------- | -------------------------------------- |
| Python 3.12           | Linguagem principal                    |
| Django 5.2            | Framework backend                      |
| Django REST Framework | Desenvolvimento da API REST            |
| PostgreSQL 17         | Banco de dados relacional              |
| Psycopg 3             | Driver de conexão com PostgreSQL       |
| Requests              | Requisições HTTP para API externa      |
| OpenWeather API       | Fonte de dados meteorológicos          |
| drf-spectacular       | Documentação OpenAPI/Swagger           |
| python-decouple       | Gerenciamento de variáveis de ambiente |
| Docker                | Containerização                        |
| Docker Compose        | Orquestração dos serviços              |
| Git                   | Controle de versão                     |

## Arquitetura

A aplicação está organizada de forma modular, separando as responsabilidades de integração externa, persistência de dados, serialização e exposição das informações através dos endpoints REST.

- **Services:** comunicação com a API OpenWeather, tratamento de erros e transformação dos dados recebidos.
- **Models:** representação e persistência dos registros meteorológicos no PostgreSQL.
- **Serializers:** validação e conversão dos dados entre objetos Python e JSON.
- **Views:** coordenação das operações HTTP e integração entre serviços, serializers e models.
- **URLs:** mapeamento dos endpoints da aplicação.

## Banco de dados

O projeto utiliza PostgreSQL 17, executado em container Docker através do Docker Compose.

### Configuração

| Parâmetro     | Valor         |
| ------------- | ------------- |
| SGBD          | PostgreSQL 17 |
| Database      | weather_db    |
| Usuário       | weather_user  |
| Porta externa | 5434          |
| Porta interna | 5432          |
| Container     | weather-db    |

### Persistência dos dados

Os dados são armazenados em um volume Docker nomeado:

`postgres_data`

Isso permite preservar os dados mesmo após a parada ou recriação do container.

### Conexão pelo pgAdmin

Para acessar o banco utilizando o pgAdmin:

- Host: `localhost`
- Port: `5434`
- Database: `weather_db`
- Username: `weather_user`
- Password: definida no arquivo `.env`

### Modelo meteorológico

Foi criado o modelo `WeatherRecord`, responsável por representar os registros meteorológicos armazenados no banco de dados.

O modelo contempla as seguintes informações:

- Cidade e país.
- Temperatura e sensação térmica.
- Umidade.
- Pressão atmosférica.
- Velocidade do vento.
- Descrição das condições meteorológicas.
- Data e hora da observação.
- Data e hora de criação do registro.

A tabela foi criada através de migrations do Django.

## API REST

A API REST foi desenvolvida utilizando Django REST Framework, permitindo consultar os registros meteorológicos armazenados no PostgreSQL e realizar novas coletas através da OpenWeather.

### Listar registros meteorológicos

**Método:** `GET`

**Endpoint:** `/api/weather/`

Retorna todos os registros meteorológicos cadastrados.

### Filtrar registros por cidade

O endpoint `GET /api/weather/` permite filtrar os registros pelo nome da cidade utilizando o parâmetro `city`.

A busca utiliza a extensão `unaccent` do PostgreSQL em conjunto com `icontains`, permitindo localizar cidades independentemente de acentos e letras maiúsculas ou minúsculas.

Exemplos:

```http
GET /api/weather/?city=Florianópolis
GET /api/weather/?city=Florianopolis
GET /api/weather/?city=FLORIANOPOLIS
```

O filtro utiliza correspondência parcial. Quando o parâmetro `city` não é informado, todos os registros são retornados. Caso nenhum registro corresponda ao filtro, a API retorna uma lista vazia.

### Coletar dados meteorológicos

**Método:** `POST`

**Endpoint:** `/api/weather/collect/`

Realiza uma consulta à API OpenWeather para obter informações meteorológicas da cidade informada e armazena os dados retornados no PostgreSQL.

**Exemplo de requisição:**

```http
POST /api/weather/collect/
Content-Type: application/json
```

```json
{
  "city": "Florianópolis"
}
```

**Exemplo de resposta:**

```json
{
  "id": 2,
  "city": "Florianópolis",
  "country": "BR",
  "temperature": "26.43",
  "feels_like": "26.43",
  "humidity": 80,
  "pressure": 1008,
  "wind_speed": "7.20",
  "description": "algumas nuvens",
  "observed_at": "2026-11-18T10:50:33-03:00",
  "created_at": "2026-11-18T10:52:12-03:00"
}
```

Os valores retornados podem variar conforme as condições meteorológicas no momento da consulta.

### Respostas HTTP

| Código                  | Descrição                                                    |
| ----------------------- | ------------------------------------------------------------ |
| 201 Created             | Dados coletados e armazenados com sucesso                    |
| 400 Bad Request         | Nome da cidade ausente ou inválido                           |
| 404 Not Found           | Cidade não encontrada na OpenWeather                         |
| 502 Bad Gateway         | Falha de autenticação na integração com a OpenWeather        |
| 503 Service Unavailable | Falha de comunicação ou indisponibilidade do serviço externo |

### Integração com OpenWeather

A integração utiliza o endpoint de consulta meteorológica atual da OpenWeather:

`https://api.openweathermap.org/data/2.5/weather`

Os parâmetros utilizados são:

| Parâmetro | Descrição                     |
| --------- | ----------------------------- |
| `q`       | Nome da cidade consultada     |
| `appid`   | Chave de autenticação da API  |
| `units`   | Unidade de medida (`metric`)  |
| `lang`    | Idioma da descrição (`pt_br`) |

A chave de API é configurada através da variável de ambiente `OPENWEATHER_API_KEY`, armazenada no arquivo `.env`.

A aplicação trata erros de comunicação, timeout, autenticação, limite de requisições e cidades não encontradas.

## Documentação OpenAPI

A API possui documentação interativa utilizando OpenAPI e drf-spectacular.

| Recurso        | Endpoint       |
| -------------- | -------------- |
| Swagger UI     | `/api/docs/`   |
| OpenAPI Schema | `/api/schema/` |

O schema pode ser disponibilizado nos formatos YAML e JSON.

## Testes automatizados

O projeto utiliza o framework de testes nativo do Django, com suporte do `unittest.mock` para simular a integração com serviços externos.

Os testes verificam o comportamento dos endpoints REST, o tratamento de erros e a persistência dos registros no banco de dados.

### Cenários testados

| Teste                             | Resultado esperado           |
| --------------------------------- | ---------------------------- |
| Coleta meteorológica bem-sucedida | HTTP 201 Created             |
| Cidade não encontrada             | HTTP 404 Not Found           |
| Serviço externo indisponível      | HTTP 503 Service Unavailable |
| Listagem de registros             | HTTP 200 OK                  |
| Filtro de registros por cidade    | HTTP 200 OK                  |

A integração com a OpenWeather é simulada utilizando `unittest.mock.patch`, permitindo testar os diferentes cenários sem realizar chamadas reais à API externa.

O Django cria um banco de dados exclusivo para os testes, executa os cenários e o remove ao finalizar.

## Execução do projeto

### Pré-requisitos

- Docker.
- Docker Compose.
- Conta na [OpenWeather](https://openweathermap.org/) e chave de API.

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd weather-data-api
```

### 2. Configurar as variáveis de ambiente

Crie o arquivo `.env` a partir do exemplo disponibilizado:

```bash
cp .env.example .env
```

Configure as variáveis necessárias:

```env
SECRET_KEY=sua_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=weather_db
DB_USER=weather_user
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5434

OPENWEATHER_API_KEY=sua_chave_openweather
```

Substitua os valores de exemplo pelas suas configurações.

**Importante:** o arquivo `.env` contém informações sensíveis e não deve ser versionado no Git.

### 3. Construir e iniciar os containers

Na raiz do projeto, execute:

```bash
docker compose up -d --build
```

O Docker Compose será responsável por construir a imagem da aplicação Django e iniciar os serviços:

- `web`: aplicação Django.
- `db`: banco de dados PostgreSQL.

O serviço Django aguarda a inicialização saudável do PostgreSQL antes de iniciar.

### 4. Habilitar a extensão Unaccent

A aplicação utiliza a extensão `unaccent` do PostgreSQL para realizar buscas sem distinção de acentos.

Execute o comando:

```bash
docker compose exec db psql -U weather_user -d weather_db -c "CREATE EXTENSION IF NOT EXISTS unaccent;"
```

A extensão deve estar habilitada no banco utilizado pela aplicação.

### 5. Executar as migrations

Para criar as tabelas necessárias no banco de dados:

```bash
docker compose exec web python manage.py migrate
```

### 6. Verificar os containers

```bash
docker compose ps
```

Para consultar os logs da aplicação:

```bash
docker compose logs web
```

Para consultar os logs do banco:

```bash
docker compose logs db
```

### 7. Acessar a aplicação

Após iniciar os serviços, a API estará disponível em:

- API: `http://localhost:8000/api/weather/`
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

### 8. Executar os testes

Com os containers em execução:

```bash
docker compose exec web python manage.py test weather
```

O Django executará os testes utilizando um banco de dados exclusivo para essa finalidade.

### 9. Parar os containers

Para parar os serviços:

```bash
docker compose down
```

Os dados do PostgreSQL permanecem armazenados no volume `postgres_data`.

**Atenção:** evite utilizar `docker compose down -v` quando desejar preservar os dados, pois essa opção remove os volumes associados ao projeto.

## Status do projeto

Implementação concluída para os requisitos propostos.

### Funcionalidades implementadas

- Configuração do Django e Django REST Framework.
- Configuração do PostgreSQL com Docker Compose.
- Containerização da aplicação Django.
- Modelagem e persistência dos dados meteorológicos.
- Integração com a API OpenWeather.
- Transformação dos dados recebidos.
- Tratamento de erros da integração externa.
- Endpoint GET para listagem e filtro por cidade.
- Endpoint POST para coleta e armazenamento de dados.
- Validação e persistência utilizando Django REST Framework.
- Testes automatizados dos endpoints e integração externa.
- Documentação interativa da API com Swagger/OpenAPI.
- Filtro de cidades sem distinção de acentos utilizando a extensão `unaccent` do PostgreSQL.
- Execução integrada da aplicação e banco de dados com Docker Compose.
