from sqlalchemy import Table, Column, Integer, String, ForeignKey
from app.config.db1 import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .category_model import CategoryDB
from .user_model import UserDB


association_table = Table(
    "password_tag_association",
    Base.metadata,
    Column("password_id", Integer, ForeignKey("password.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class PasswordDB(Base):
    __tablename__ = "password"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    category: Mapped[CategoryDB] = relationship(back_populates="passwords")
    user: Mapped[UserDB] = relationship(back_populates="passwords")

    tags = relationship(
        "TagDB", secondary=association_table, back_populates="passwords"
    )
