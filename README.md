# Weather Data API

API REST desenvolvida em Python com Django REST Framework para coleta, armazenamento e consulta de dados meteorológicos utilizando a API pública da OpenWeather.

O projeto tem como objetivo integrar uma fonte externa de dados, processar as informações recebidas e armazená-las em um banco de dados relacional, disponibilizando endpoints para consulta do histórico meteorológico.

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

A aplicação está sendo organizada de forma modular, separando as responsabilidades de persistência de dados, serialização e exposição das informações através dos endpoints REST.

A integração com serviços externos será isolada em uma camada de serviços, mantendo a lógica de comunicação com a API OpenWeather separada das Views.

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

### Executar o banco de dados

Na raiz do projeto, execute:

```bash
docker compose up -d
```

Para verificar o status do container:

```bash
docker compose ps
```

Para consultar os logs:

```bash
docker compose logs db
```

### Conexão pelo pgAdmin

Para acessar o banco utilizando o pgAdmin:

- Host: `localhost`
- Port: `5434`
- Database: `weather_db`
- Username: `weather_user`
- Password: definida no arquivo `.env`

### Persistência dos dados

Os dados são armazenados em um volume Docker nomeado:

`postgres_data`

Isso permite preservar os dados mesmo após a parada ou recriação do container.

### Integração com Django

A conexão entre Django e PostgreSQL é configurada através de variáveis de ambiente, utilizando `python-decouple`.

As configurações incluem:

- Nome do banco de dados.
- Usuário e senha.
- Host e porta de conexão.

As migrations iniciais do Django foram executadas com sucesso, criando as tabelas necessárias para os recursos internos do framework.

Para aplicar migrations:

```bash
python manage.py migrate
```

### Modelo meteorológico

Foi criado o modelo `WeatherRecord`, responsável por representar os registros meteorológicos armazenados no banco de dados.

O modelo contempla informações de cidade, país, temperatura, sensação térmica, umidade, pressão atmosférica, velocidade do vento, descrição e datas de observação e criação.

A tabela foi criada através de migrations do Django.

A persistência foi validada utilizando o Django ORM, com inserção e consulta de registros no PostgreSQL.

## Documentação da API

## API REST

A API REST foi desenvolvida utilizando Django REST Framework, permitindo consultar os registros meteorológicos armazenados no PostgreSQL.

### Listar registros meteorológicos

**Endpoint:** `GET /api/weather/`

Retorna todos os registros meteorológicos cadastrados.

**Exemplo de resposta:**

```json
[
  {
    "id": 1,
    "city": "Florianópolis",
    "country": "BR",
    "temperature": "24.19",
    "feels_like": "24.78",
    "humidity": 81,
    "pressure": 1010,
    "wind_speed": "6.69",
    "description": "nublado",
    "observed_at": "2026-11-17T18:43:39-03:00",
    "created_at": "2026-11-17T18:43:48-03:00"
  }
]
```

### Filtrar registros por cidade

O endpoint permite filtrar os registros através do parâmetro de consulta `city`.

**Exemplo:**

`GET /api/weather/?city=Florianópolis`

O filtro utiliza correspondência parcial e não diferencia letras maiúsculas e minúsculas.

Quando o parâmetro `city` não é informado, todos os registros são retornados.

Caso nenhum registro corresponda ao filtro, a API retorna uma lista vazia.

### Documentação OpenAPI

A documentação interativa dos endpoints será disponibilizada através do Swagger UI, utilizando OpenAPI e drf-spectacular.

## Execução

As instruções de instalação, configuração do ambiente, inicialização dos serviços e utilização da API serão documentadas conforme o desenvolvimento do projeto.

## Status do projeto

Em desenvolvimento.
