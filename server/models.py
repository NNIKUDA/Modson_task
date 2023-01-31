from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base, engine


class Document(Base):
    __table__ = Table(
        "docs",
        Base.metadata,
        autoload_with=engine,
    )

    def __init__(self, id, text, date_of_writing, rubrics):
        self.id = id
        self.text = text
        self.date_if_writing = date_of_writing
        self.rubrics = rubrics

