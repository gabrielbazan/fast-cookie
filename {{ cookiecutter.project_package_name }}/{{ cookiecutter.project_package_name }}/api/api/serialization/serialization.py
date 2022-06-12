from typing import Any, Dict, List, Tuple

from database import Base, Session
from fastapi import HTTPException, status
from serialization.base_models import PaginatedListField
from sqlalchemy.orm.exc import NoResultFound


def paginate_list(
    session: Session,
    model: Base,
    offset: int,
    limit: int,
    order_by: List = None,
    filters: List = None,
) -> Dict:
    total_count_query, results_query = build_queries(
        session, model, offset, limit, order_by, filters
    )

    results = results_query.all()

    return {
        PaginatedListField.TOTAL_COUNT: total_count_query.count(),
        PaginatedListField.COUNT: len(results),
        PaginatedListField.LIMIT: limit,
        PaginatedListField.OFFSET: offset,
        PaginatedListField.RESULTS: results,
    }


def build_queries(
    session: Session,
    model: Base,
    offset: int,
    limit: int,
    order_by: List,
    filters: List,
) -> Tuple:
    total_count_query = session.query(model)
    if filters:
        total_count_query = total_count_query.filter(*filters)

    results_query = total_count_query
    if order_by:
        results_query = results_query.order_by(*order_by)
    results_query = results_query.offset(offset).limit(limit)

    return total_count_query, results_query


def read(session: Session, model: Base, identifier: Any) -> Base:
    instance = session.query(model).filter(model.id == identifier).one_or_none()

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return instance


def get_or_raise(session: Session, model: Base, **kwargs) -> Base:
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} not found: {kwargs}",
        )
