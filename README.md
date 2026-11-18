# Weather Data API

API REST desenvolvida em Python com Django REST Framework para coleta, armazenamento e consulta de dados meteorológicos utilizando a API pública da [OpenWeather](https://openweathermap.org/api).

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

A aplicação está organizada de forma modular, separando as responsabilidades de integração externa, persistência de dados, serialização e exposição das informações através dos endpoints REST.

A estrutura utiliza as seguintes responsabilidades:

- **Services:** responsável pela comunicação com a API OpenWeather, tratamento de erros e transformação dos dados recebidos.
- **Models:** responsável pela representação e persistência dos registros meteorológicos no PostgreSQL.
- **Serializers:** responsável pela validação e conversão dos dados entre objetos Python e JSON.
- **Views:** responsável por coordenar as operações HTTP e integrar os serviços, serializers e models.
- **URLs:** responsável pelo mapeamento dos endpoints da aplicação.

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

As migrations iniciais do Django foram executadas com sucesso, criando as tabelas necessárias para os recursos internos do framework e para o modelo meteorológico.

Para aplicar migrations:

```bash
python manage.py migrate
```

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

A persistência foi validada utilizando o Django ORM, com inserção e consulta de registros no PostgreSQL.

## API REST

A API REST foi desenvolvida utilizando Django REST Framework, permitindo consultar os registros meteorológicos armazenados no PostgreSQL e realizar novas coletas através da OpenWeather.

### Listar registros meteorológicos

**Método:** `GET`

**Endpoint:** `/api/weather/`

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

```http
GET /api/weather/?city=Florianópolis
```

O filtro utiliza correspondência parcial e não diferencia letras maiúsculas e minúsculas.

Quando o parâmetro `city` não é informado, todos os registros são retornados.

Caso nenhum registro corresponda ao filtro, a API retorna uma lista vazia.

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

**Respostas HTTP:**

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

A documentação interativa dos endpoints será disponibilizada através do Swagger UI, utilizando OpenAPI e `drf-spectacular`.

## Execução

As instruções completas de instalação, configuração do ambiente, inicialização da aplicação e utilização da API serão documentadas conforme a conclusão das etapas de desenvolvimento.

## Status do projeto

Em desenvolvimento.

### Implementado

- Configuração do Django e Django REST Framework.
- Configuração do PostgreSQL com Docker Compose.
- Modelagem e persistência dos dados meteorológicos.
- Integração com a API OpenWeather.
- Transformação dos dados recebidos.
- Tratamento de erros da integração externa.
- Endpoint GET para listagem e filtro por cidade.
- Endpoint POST para coleta e armazenamento de dados.
- Validação e persistência utilizando Django REST Framework.

### Próximas etapas

- Implementação de testes automatizados.
- Configuração da documentação Swagger/OpenAPI.
- Containerização da aplicação Django.
- Finalização das instruções de execução.
