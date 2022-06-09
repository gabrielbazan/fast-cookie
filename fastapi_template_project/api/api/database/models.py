from sqlalchemy import Column, Integer, Text
from database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)

    name = Column(Text)
