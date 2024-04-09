from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

from .password import association_table


class TagDB(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    slug = Column(String)

    passwords = relationship(
        "PasswordDB", secondary=association_table, back_populates="tags"
    )
