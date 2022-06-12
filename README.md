# FastAPI Project Template

Tired of re-inventing the wheel everytime you need to start a project? If you're
starting a brand new [FastAPI](https://fastapi.tiangolo.com/) project, this is for you!


## What's in it


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

## How do I check if my new project is working?

Open any browser, or CURL, or 