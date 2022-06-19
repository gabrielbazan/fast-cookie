# Fast Cookie

Tired of reinventing the wheel everytime you start a [FastAPI](https://fastapi.tiangolo.com/) project? 
This is for you!


## About

Fast Cookie is a FastAPI project generator you can use to quickly start turning your idea into reality, without 
reinventing the wheel. 

You don't have to worry about how to organize, dockerize, and configue your new project. Not even how to add and run
unit tests, or how to install GIT hooks. You get all that from the very beginning.

If you need a relational database, you don't even have to worry about that. You can start with a dockerized relational
database, database migrations, session management methods, and serialization methods for your API.


## Stack

### Language

 * [Python3.10](https://www.python.org/downloads/release/python-3100/)


### Containerization

 * [Docker](https://www.docker.com/)
 * [Docker compose](https://docs.docker.com/compose/)


### Web framework

 * [FastAPI](https://fastapi.tiangolo.com/)


### Git hooks

 * [Black](https://github.com/psf/black)
 * [Isort](https://github.com/PyCQA/isort)
 * [Flake8](https://github.com/PyCQA/flake8)


### Database migrations

If you choose to have a relational database, you get: 
 * [SQLAlchemy](https://www.sqlalchemy.org/)
 * [Alembic](https://alembic.sqlalchemy.org/en/latest/) database migrations
 * A [PostgreSQL](https://www.postgresql.org/) dockerized instance. As this template uses SQLAlchemy, you can pretty
    sure change it for any other RDBMS.


## Get your project started

Just [install cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html) 
and run this (SSH):
```shell
cookiecutter git+ssh://git@github.com/gabrielbazan/fastapi_template_project.git
```

Or this (HTTPS):
```shell
cookiecutter https://github.com/gabrielbazan/fastapi_template_project.git
```

You'll be prompted to enter a few project config values:
 * Project name
 * Project package name
 * Host port number for your API
 * Whether you need a relational database or not


## Run your project

After creating your project from this template, just go to the docker-compose directory and start the containers:
```shell
cd {project_package_name}/{project_package_name}
docker compose up
```

And that's all. Your new API is now running in the port you've specified.


## Take a look at your running API

Hit the API root with any browser. For example, with CURL:
```shell
curl localhost:{api_port}
```

Check the API docs! http://localhost:{api_port}/docs

And the alternative API docs! http://localhost:{api_port}/redoc


## Set the repo up

First, create the new repo in GitHub, GitLab, BitBucket, or whatever.

Then, init the local repo:
```shell
git init
```

If you wish to use the local GIT hooks, install them:
```shell
python -m pip install pre-commit
pre-commit install
```

Add all your changes and commit. If you've installed the local hooks, on the first commit ``pre-commit`` will 
create their isolated environments and will take a short while on the first run. Subsequent checks will be 
significantly faster.
```shell
git add -A
git commit -m "First commit"
```

Create your branch (I'll use 'main' in this example), add the remote and push:
```shell
git branch -M main
git remote add origin git@github.com:{your_user}/{project_package_name}.git
git push -u origin main
```


## Ok cool, so how do I add my awesome things?

### Configuring the service


### Adding database models

```python
from sqlalchemy import Column, Integer, Text
from database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)

    name = Column(Text)
```


### Adding database migrations

```shell
cd {project_package_name}/{project_package_name}/api/api
./generate_alembic_migration.sh "Add 'todo' table"
```


### Adding serialization models

```python
from typing import List
from pydantic import BaseModel
from serialization.base_models import BasePaginatedList


class TodoModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class TodoCreateOrEdit(BaseModel):
    name: str


class TodoPaginatedList(BasePaginatedList):
    results: List[TodoModel]
```


### Adding routers

```python
from pydantic import BaseSettings


class Settings(BaseSettings):
    ...

    todos_route: str = "/todos"
    todos_tag: str = "Todos"

    ...
```


```python
from fastapi import APIRouter
from settings import settings


router = APIRouter(prefix=settings.todos_route, tags=[settings.todos_tag])
```


```python
from typing import List
from fastapi import APIRouter
from . import todos


# Add your APIRouters to this list
ALL_ROUTERS: List[APIRouter] = [todos.router, ]
```


### Adding endpoints

```python
from fastapi import Depends
from settings import settings, ROOT_ROUTE
from database import Session, session_scope
from database.models import Todo
from serialization.serialization import paginate_list
from serialization.models import TodoPaginatedList


@router.get(ROOT_ROUTE, response_model=TodoPaginatedList)
def list_todos(
    limit: int = settings.default_limit,
    offset: int = settings.default_offset,
    session: Session = Depends(session_scope),
):
    return paginate_list(session, Todo, offset, limit)
```


```python
from fastapi import Depends, status
from settings import ROOT_ROUTE
from database import Session, session_scope
from database.models import Todo
from serialization.models import TodoModel, TodoCreateOrEdit


@router.post(
    ROOT_ROUTE, response_model=TodoModel, status_code=status.HTTP_201_CREATED
)
def create_todo(
    todo: TodoCreateOrEdit, session: Session = Depends(session_scope)
):
    todo_orm = Todo(**todo.dict())
    session.add(todo_orm)
    session.flush()

    return todo_orm
```


```python
from fastapi import Depends
from settings import IDENTIFIER_ROUTE
from database import Session, session_scope
from database.models import Todo
from serialization.serialization import get_or_raise
from serialization.models import TodoModel


@router.get(IDENTIFIER_ROUTE, response_model=TodoModel)
def read_todo(identifier: int, session: Session = Depends(session_scope)):
    return get_or_raise(session, Todo, id=identifier)
```


```python
from fastapi import Depends
from settings import IDENTIFIER_ROUTE
from database import Session, session_scope
from database.models import Todo
from serialization.serialization import get_or_raise
from serialization.models import TodoModel, TodoCreateOrEdit


@router.put(IDENTIFIER_ROUTE, response_model=TodoModel)
def update_todo(
    identifier: int,
    todo: TodoCreateOrEdit,
    session: Session = Depends(session_scope),
):
    instance = get_or_raise(session, Todo, id=identifier)

    instance.name = todo.name

    session.add(instance)

    return instance
```


```python
from fastapi import Depends, status, Response
from settings import IDENTIFIER_ROUTE
from database import Session, session_scope
from database.models import Todo
from serialization.serialization import get_or_raise


@router.delete(IDENTIFIER_ROUTE, status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(identifier: int, session: Session = Depends(session_scope)):
    instance = get_or_raise(session, Todo, id=identifier)
    session.delete(instance)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```


### Adding unit tests

### Running unit tests

```shell
cd {project_package_name}/{project_package_name}/api/api
./run_unit_tests.sh
```
