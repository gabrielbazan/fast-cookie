from fastapi import APIRouter, Depends, status
from settings import settings
from database import Session, session_scope
from database.models import Todo
from common import ROOT_ROUTE, IDENTIFIER_ROUTE, paginate_list, read, get_or_raise
from serialization.models import TodoModel, TodoCreateOrEdit, TodoPaginatedList


router = APIRouter(prefix=settings.todos_route, tags=[settings.todos_tag])


@router.get(ROOT_ROUTE, response_model=TodoPaginatedList)
def list_todos(
    limit: int = settings.default_limit,
    offset: int = settings.default_offset,
    session: Session = Depends(session_scope),
):
    return paginate_list(session, Todo, offset, limit)


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


@router.get(IDENTIFIER_ROUTE, response_model=TodoModel)
def read_todo(identifier: int, session: Session = Depends(session_scope)):
    return read(session, Todo, identifier)


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


@router.delete(IDENTIFIER_ROUTE, status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(identifier: int, session: Session = Depends(session_scope)):
    instance = get_or_raise(session, Todo, id=identifier)
    session.delete(instance)
