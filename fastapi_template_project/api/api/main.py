from typing import List
from fastapi import FastAPI, APIRouter
from routers import ALL_ROUTERS
from cors import configure_cors


def create_app():
    fast_api_app = FastAPI()
    configure_cors(fast_api_app)
    include_routers(fast_api_app, ALL_ROUTERS)
    return fast_api_app


def include_routers(app: FastAPI, routers: List[APIRouter]) -> None:
    for router in routers:
        app.include_router(router)


app = create_app()


@app.get("/")
def root():
    return {"discovery": "API"}
