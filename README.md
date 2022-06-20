# Fast Cookie

Tired of reinventing the wheel everytime you start a [FastAPI](https://fastapi.tiangolo.com/) project? 
This is for you!


## About

Everytime people need to start a new project, they have to figure out the best ways to do things like: How to organize
the project structure, and how to dockerize, how to run, how to connect with a database, handle sessions, validate,
serialize data, configure the service, requirements, virtual environments, run unit tests, lint, check code styling, 
GIT hooks, and the list goes on...

Fast Cookie is a FastAPI project generator that takes care of all these things beforehand, so you can quickly start 
making your idea come true, without reinventing the wheel. You get all that from the very beginning.


## Stack

### Language

 * [Python3.10](https://www.python.org/downloads/release/python-3100/)


### Containerization

 * [Docker](https://www.docker.com/)
 * [Docker compose](https://docs.docker.com/compose/)


### Web framework

 * [FastAPI](https://fastapi.tiangolo.com/)


### Git hooks

 * [Pre-commit](https://pre-commit.com/)
 * [Black](https://github.com/psf/black)
 * [Isort](https://github.com/PyCQA/isort)
 * [Flake8](https://github.com/PyCQA/flake8)


### Relational database, ORM, and migrations

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
 * Project name (_project_name_): The human-friendly name of your project. Example: "TODO List Admin"
 * Project package name (_project_package_name_): The Python package name that will contain the code. Example: "todo_list_admin"
 * Host port number for your API (_api_port_): Host port where the API will be available when the project is up.
 * Whether you need a relational database or not (_add_database_): Whether you need a relational database in your project or not.


## Set the repo up

First, create the new repo in GitHub, GitLab, BitBucket, or whatever.

Then, go into your new project's folder:
```shell
cd {project_package_name}
```

And init the local repo:
```shell
git init
```

If you wish to use the local GIT hooks, install them:
```shell
python3 -m pip install pre-commit
pre-commit install
```

Add all your changes and commit. If you've installed the local hooks, on the first commit ``pre-commit`` will 
create their isolated environments and will take a short while on the first run. Subsequent checks will be 
significantly faster.
```shell
git add -A
git commit -m "First commit"
```

Create your branch (I'll use 'main' in this example), add the remote, and push:
```shell
git branch -M main
git remote add origin git@github.com:{your_user}/{project_package_name}.git
git push -u origin main
```


## Run your project

From you new repo's root, just go to the docker-compose directory and start the containers:
```shell
cd {project_package_name}/
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


## Create the virtualenv

You can install the API's requirements, and its test requirements, in a virtualenv. This way, you can keep your system
interpreter clean. You can then use this virtualenv to run unit tests, and also configure your IDE to inspect packages 
from there (for autocompletion and such).

First, go to the API directory:
```shell
cd api/api/
```

If you use Ubuntu and don't have _python-venv_ installed, install it:
```shell
make install_venv
```

To create the virtualenv, run:
```shell
make create_venv
```

To install the requirements:
```shell
make install_reqs_in_venv
```

And to install the test requirements:
```shell
make install_test_reqs_in_venv
```

## Run unit tests

The template comes with some unit tests, which you can already run. As you add unit tests, you can run them the same
way.

First, make sure you're in the API directory:
```shell
cd api/api/
```

After creating the virtualenv, and installed the requirements (including test requirements), run the following to run 
all unit tests:
```shell
make run_unit_tests
```


## Make your idea come true

If, when creating your project from the template, you've decided to include a relational database, you'll have a 
containerized PostgreSQL instance, along with Alembic migrations and a bunch of very useful methods in your API, 
such as for session management, validation, serialization, and pagination.


### Add API endpoints, without a relational database

You can make your API do literally anything. Say we want to add a few endpoints to manage a TODO list. In FastAPI, 
endpoints are grouped by routers. Then all we need to do is to add a router, register it to the API, and add endpoints 
to it.


#### Add a new router

It's probably convenient to make our URI paths configurable in our API. You could just hardcode them, but say we want 
to be able to change them in our settings file 
([settings.env](/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/api/api/settings.env)), 
with absolutely no impact in our code. Then on 
([settings.py](/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/api/api/settings.py)) 
we'll add two new settings. One for the URI path (_todos_route_), and another to give the route a human-readable name for the API documentation 
(_todos_tag_). These are default values, meaning that if you change them in _settings.env_, the values in that file will be used instead.

```python
from pydantic import BaseSettings


class Settings(BaseSettings):
    ...
    todos_route: str = "/todos"
    todos_tag: str = "Todos"
    ...
```

Then we'll add a new _todos.py_ module in 
[routers](/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/api/api/routers), 
and add our new router with configurable path and tag:

```python
from fastapi import APIRouter
from settings import settings


router = APIRouter(prefix=settings.todos_route, tags=[settings.todos_tag])
```

And then all that's left is register our router in the API, which is done by adding it to a list in 
[routers/__init__.py](/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/api/api/routers/__init__.py):

```python
from typing import List
from fastapi import APIRouter
from . import todos


# Add your APIRouters to this list
ALL_ROUTERS: List[APIRouter] = [todos.router, ]
```


#### Add a new endpoint

Say we want to add an endpoint to list TODOs.

First, we'll need to create a couple of models so that we can serialize our data, and document its structure so that
people can check our docs and know what to expect when they use our endpoints.

So we add a _todo_models.py_ in the 
[serialization](/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/api/api/serialization)
package, with a couple of models:
```python
from typing import List
from pydantic import BaseModel
from serialization.base_models import BasePaginatedList


class TodoModel(BaseModel):
    id: int
    name: str


class TodoPaginatedList(BasePaginatedList):
    results: List[TodoModel]
```

Then, we add the endpoint to the router, in _routers/todos.py_:

```python
from serialization.todo_models import TodoPaginatedList
from settings import ROOT_ROUTE, settings


@router.get(ROOT_ROUTE, response_model=TodoPaginatedList)
def list_todos(
    limit: int = settings.default_limit,
    offset: int = settings.default_offset,
):
    # TODO: ... work your galactic magic here ...
    return {
        "results": [
            {
                "id": 1,
                "name": "Feed the cat",
            }
        ],
        "total_count": 1,
        "count": 1,
        "limit": limit,
        "offset": offset,
    }
```


### Add API endpoints, without a relational database

#### Adding database models

```python
from sqlalchemy import Column, Integer, Text
from database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)

    name = Column(Text)
```


#### Adding database migrations

```shell
cd {project_package_name}/{project_package_name}/api/api
./generate_alembic_migration.sh "Add 'todo' table"
```


#### Adding serialization models

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


#### Adding routers

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


#### Adding endpoints

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


### Configuring the API service


### Adding unit tests
