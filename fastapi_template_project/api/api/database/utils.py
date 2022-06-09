from database import Session, Base


def exists(session: Session, model: Base, **kwargs) -> bool:
    return session.query(session.query(model).filter_by(**kwargs).exists()).scalar()
