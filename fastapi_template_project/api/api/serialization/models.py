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
