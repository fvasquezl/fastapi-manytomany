from typing import List
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from app.config.db1 import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

from .password_model import association_table


class TagDB(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)

    passwords = relationship(
        "PasswordDB", secondary=association_table, back_populates="tags"
    )
