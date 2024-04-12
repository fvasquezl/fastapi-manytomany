from typing import List
from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    create_engine,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime


DATABASE_URL = "sqlite:///./test.db"

Model = declarative_base()


class NotFoundError(Exception):
    pass


class Base(Model):
    __abstract__ = True
    created_at = mapped_column(DateTime(timezone=True), default=datetime.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=datetime.now())


class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True,)
    post: Mapped[str] = mapped_column(nullable=False)

    """relationship many to many to Roles"""
    roles :Mapped[list["DBRole"]] = relationship(secondary="users_roles", back_populates="users", passive_deletes=True)

    """relationship one to many to Posts"""
    posts: Mapped[List["DBPost"]] = relationship(back_populates="user", passive_deletes=True)


"""Asociation Table Users-Roles"""
class DBUserRole(Base):
    __tablename__ = "users_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)



class DBRole(Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    """relationship many to many to Users"""
    users: Mapped[List["DBUser"]] = relationship(secondary="users_roles",back_populates="roles", passive_deletes=True)
    


class DBCategory(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    """relationship one to many to Posts"""
    posts: Mapped[List["DBPost"]] = relationship(back_populates="category")



class DBPost(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    description: Mapped[str]

    """Relationship Many to One To Category"""
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"),nullable=False,index=True,unique=True)
    category: Mapped["DBCategory"] = relationship(back_populates="posts")

    """Relationship Many to One To User"""
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False,index=True,unique=True)
    user: Mapped["DBUser"] = relationship(back_populates="posts")

    """Relationship Many to May To Tag"""
    tags: Mapped[List["DBTag"]] = relationship(secondary="posts_tags", back_populates="posts",passive_deletes=True)



"""Asociation Table Post-Tag"""
class DBPostTag(Base):
    __tablename__ = "posts_tags"

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True)



class DBTag(Model):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    """Relationship Many to Many To Post"""
    posts: Mapped[List["DBPost"]] = relationship(secondary="posts_tags", back_populates="tags",passive_deletes=True)


engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()


#https://michaelcho.me/article/using-model-callbacks-in-sqlalchemy-to-generate-slugs/