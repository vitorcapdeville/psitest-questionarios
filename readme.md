# Serviço de questionário

Este serviço é responsável por disponibilizar questionários psicológicos para o frontend. O serviço armazena os questinários, com suas perguntas e alternativas de resposta a cada pergunta. A comunicação é via GraphQL, permitindo uma busca precisa pelas informações disponíveis.

## Instalação local

Para utilizar o serviço localmente, é recomendado a criação de um ambiente virtual.

```bash
python -m venv .venv
.venv/scripts/activate
```

Após a criação do ambiente virtual, instale as dependências do projeto.

```bash
pip install -r requirements.txt
```

### Execução

Antes de executar o servidor, é necessário inicializar o banco de dados:

```bash
python ./create_db.py
```

Para executar o servidor, utilize o comando:

```bash
fastapi run app --port 8004
```

O servidor estará disponível em `http://localhost:8004`.

## Utilizando via Docker

Para executar via Docker, é necessário ter o Docker instalado e em execução. Também é necessário que exista uma rede chamada `psitest`. A rede deve ser criada uma única vez com o seguinte comando:

```bash
docker network create psitest
```

Após a criação da rede, execute o seguinte comando para criar a imagem do serviço:

```bash
docker compose up
```

O serviço estará disponível em `http://localhost:8004`.

