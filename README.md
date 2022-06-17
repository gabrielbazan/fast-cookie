# Fast Cookie - FastAPI Boilerplate

Tired of reinventing the wheel everytime you start a new [FastAPI](https://fastapi.tiangolo.com/) project? 
This is for you!


## About

It is a starting point to quickly start building your app without reinventing the wheel, and therefore focusing 
on becoming your idea true, while keeping good practices and having a well-organized project.

You start with a dockerized FastAPI API, with CORS, unit tests, a cool way to configure it, and GIT hooks for 
code-formatting and code-style checking ([black](https://github.com/psf/black), [isort](https://github.com/PyCQA/isort), 
[flake8](https://github.com/PyCQA/flake8)). From there, you can scale your project depending on what you need.

If you needed, you can also start with a relational database, [Alembic](https://alembic.sqlalchemy.org/en/latest/) 
database migrations, session management methods,

By default, it comes with a [PostgreSQL](https://www.postgresql.org/) database. 
But as it uses [SQLAlchemy](https://www.sqlalchemy.org/), you can use any relational database. 
Just [change the Docker image](/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/docker-compose.yml#L12), 
and [configure it](/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/database.env).


## How do I start my project from this template?

Just [install cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html) 
and run this (SSH):
```shell
cookiecutter git+ssh://git@github.com/gabrielbazan/fastapi_template_project.git
```

Or this (HTTPS):
```shell
cookiecutter https://github.com/gabrielbazan/fastapi_template_project.git
```

You'll be prompted to enter a few project config values.


## How do I run my new project?

After creating your project from this template, just go to the docker-compose directory and
start the containers:
```shell
cd {project_package_name}/{project_package_name}
docker compose build
docker compose up
```

And that's all. Your new API is now running in the port you specified.


## How do I check if my new project is working?

Hit the API root with any browser. For example, with CURL (in the case where you're using port 5000):
```shell
curl localhost:{api_port}
```

Check the API docs! http://localhost:{api_port}/docs

And the alternative API docs! http://localhost:{api_port}/redoc


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


### Initializing the repo, committing and running git hooks

You need to init GIT before adding the hooks
```shell
git init
```

Install the pre-commit hooks:
```shell
python -m pip install pre-commit
pre-commit install
```

Add all your changes and commit. On the first commit ``pre-commit`` will install the hooks, these are installed in 
their own environments and will take a short while to install on the first run. Subsequent checks will be 
significantly faster.
```shell
git add -A
git commit -m "First commit"
```
