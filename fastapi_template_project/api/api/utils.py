from typing import List
from fastapi import FastAPI, APIRouter


def include_routers(app: FastAPI, routers: List[APIRouter]) -> None:
    for router in routers:
        app.include_router(router)
