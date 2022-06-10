from typing import List
from fastapi import FastAPI, APIRouter
from routers import ALL_ROUTERS
from cors import configure_cors


def include_routers(app: FastAPI, routers: List[APIRouter]) -> None:
    for router in routers:
        app.include_router(router)


app = FastAPI()
configure_cors(app)
include_routers(app, ALL_ROUTERS)


@app.get("/")
def root():
    return {"discovery": "API"}
