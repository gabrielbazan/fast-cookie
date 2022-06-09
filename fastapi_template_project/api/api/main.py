from fastapi import FastAPI
from routers import ALL_ROUTERS
from cors import configure_cors
from utils import include_routers


app = FastAPI()


configure_cors(app)
include_routers(app, ALL_ROUTERS)


@app.get("/")
def root():
    return {"discovery": "API"}
