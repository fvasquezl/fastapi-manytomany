from typing import List
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime


DATABASE_URL = "sqlite:///./test.db"


class NotFoundError(Exception):
    pass


class Base(DeclarativeBase):
    pass


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now()
    )

    passwords: Mapped[List["DBPassword"]] = relationship(back_populates="user")


class DBCategory(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    slug: Mapped[str]
    passwords: Mapped[List["DBPassword"]] = relationship(back_populates="category")


passwords_tags = Table(
    "password_tag_association",
    Base.metadata,
    Column("password_id", Integer, ForeignKey("password.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class DBTag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str]
    slug: Mapped[str]

    passwords: Mapped[List["DBPassword"]] = relationship(
        secondary=passwords_tags, back_populates="tags"
    )


class DBPassword(Base):
    __tablename__ = "password"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str]
    slug: Mapped[str]

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["DBCategory"] = relationship(back_populates="passwords")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["DBUser"] = relationship(back_populates="passwords")

    tags: Mapped[List["DBTag"]] = relationship(
        secondary=passwords_tags, back_populates="passwords"
    )


engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()
