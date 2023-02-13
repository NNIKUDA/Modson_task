from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base, engine


class Post(Base):
    __table__ = Table(
        "posts",
        Base.metadata,
        autoload_with=engine,
    )

    def __init__(self, id, text, created_date, rubrics):
        self.id = id
        self.text = text
        self.created_date = created_date
        self.rubrics = rubrics
