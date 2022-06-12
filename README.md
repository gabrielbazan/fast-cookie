# FastAPI Project Template

Tired of re-inventing the wheel everytime you need to start a project? If you're
starting a brand new [FastAPI](https://fastapi.tiangolo.com/) project, this is for you!


## What's in it

You can use it as a quick and well-organized point to start with your project from scratch, 
without having to reinvent the wheel. You start with an FastAPI API and a relational database, 
with Alembic database migrations and a cool way to configure your service. 
From there, you can add as many services as you may need. 

By default, it comes with a Postgres database. But as it uses [SQLAlchemy](https://www.sqlalchemy.org/), you can 
use any relational database. Just change the Docker image [here](/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/docker-compose.yml#L12),
configure it [here](/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/%7B%7B%20cookiecutter.project_package_name%20%7D%7D/database.env),
and that's it.


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

You'll be prompted to enter a few project config values, and then you're set.


## How do I run my new project?

After creating your project from this template, just go to the docker-compose directory and
start the containers:
```shell
cd {project_name}/{project_name}
docker compose build
docker compose up
```

And that's all. Your new API is running in port 5000.


## How do I check if my new project is working?

Hit the API root with any browser. For example, with CURL:
```shell
curl localhost:5000
```
