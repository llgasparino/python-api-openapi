## Criar Virtual Environment 
    python -m venv .venv

## Iniciar o Venv 
    source .venv/bin/active

## upgrade do pip
    pip install --upgrade pip

## Instalar dependencias 
    pip install -r requirements-dev.txt


# Arquivos na raiz
´´´bash
touch setup.py
touch {settings,.secrets}.toml
touch {requirements,MANIFEST}.in
touch Dockerfile.dev docker-compose.yaml
# Imagem do banco de dados
mkdir postgres
touch postgres/{Dockerfile,create-databases.sh}
# Aplicação
mkdir -p pamps/{models,routes}
touch pamps/default.toml
touch pamps/{__init__,cli,app,auth,db,security,config}.py'
touch pamps/models/{__init__,post,user}.py
touch pamps/routes/{__init__,auth,post,user}.py
# Testes
touch test.sh
mkdir tests
touch tests/{__init__,conftest,test_api}.py
├── docker-compose.yaml # Orquestração de containers
├── Dockerfile.dev # Imagem principal
├── MANIFEST.in # Arquivos incluidos na aplicação
├── requirements-dev.txt # Dependencias de ambiente dev
├── requirements.in # Dependencias de produção
├── .secrets.toml # Senhas locais
├── settings.toml # Configurações locais
├── setup.py # Instalação do projeto
├── test.sh # Pipeline de CI em ambiente dev
├── pamps
│ ├── __init__.py
│ ├── app.py # FastAPI app
│ ├── auth.py # Autenticação via token
│ ├── cli.py # Aplicação CLI `$ pamps adduser` etc
│ ├── config.py # Inicialização da config
│ ├── db.py # Conexão com o banco de dados
│ ├── default.toml # Config default
│ ├── security.py # Password Validation
│ ├── models
│ │ ├── __init__.py
│ │ ├── post.py # ORM e Serializers de posts
│ │ └── user.py # ORM e Serialziers de users
│ └── routes
│ ├── __init__.py
│ ├── auth.py # Rotas de autenticação via JWT
│ ├── post.py # CRUD de posts e likes
│ └── user.py # CRUD de user e follows
├── postgres
│ ├── create-databases.sh # Script de criação do DB
│ └── Dockerfile # Imagem do SGBD
└── tests
├── conftest.py # Config do Pytest
├── __init__.py
└── test_api.py # Tests da API
´´´
## Adicionamos ao requirements.in
´´´python
fastapi
uvicorn
sqlmodel
typer
dynaconf
jinja2
python-jose[cryptography]
passlib[bcrypt]
python-multipart
psycopg2-binary
alembic
rich
´´´

## Usamos o pip-compile para automatizar a busca de versões compativeis com a nossa versão python
    pip-compile requirements.in
Ele gera para nós o arquivo requirements.txt já com as versões.

## Criamos o MANIFEST.in
    graft pamps

## Criamos o setup.py e colocamos algumas coisas padrão, para fazer o "pamps" virar um instalador também
    pip install -e .
´´´python
setup.py
import io 
import os
from setuptools import find packages, setup 

def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname( file ), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file>
        content = open_file.read().strip()
    return content

def read requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-","git+"))
    ]


setup(
    name="pamps",
    version="0.1.0",
    description="Pamps is a social posting app",
    url="pamps.io",
    python_requires=">=3.8",
    long_description="Pamps is a social posting app",
    long_description_content_type="text/markdown",
    author="Luizão Gasparino",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["pamps = pamps.cli:main"]
    }

)
´´´
## Configuramos o arquivo Dockerfile.dev

# Subimos uma imagem docker do nosso aplicativo 
´´´bash
docker build -f Dockerfile.dev -t pamps:latest . 
docker run --rm -it -v $(pwd):/home/app/api -p 8000:8000 pamps
$ docker run -p 8000:8000 pamps
sudo setenforce 0
sudo chown -R $USER:$USER $(pwd)
´´´
# Configurando o postgres

Criamos um shell script dentro da pasta 
´´´shell
#!/bin/bash
set -e
set -u 

function creater_user_and_database(){
local database=$1
echo "Creating user and database '$database'"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER $database PASSWORD '$database';
    CREATE DATABASE $database;
    GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
EOSQL
}

if [ -n "$POSTGRES_DBS"]; then
echo "Creating DB(s): $POSTGRES_DBS"
for db in $(echo $POSTGRES_DBS | tr ',' ' '); do
    creater_user_and_database $db
done
echo "Multiple databases created"
fi 
´´´
    docker-compose up
