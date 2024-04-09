from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

association_table = Table(
    "password_tag_association",
    Base.metadata,
    Column("password_id", Integer, ForeignKey("password.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class PasswordDB(Base):
    __tablename__ = "password"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    tags = relationship(
        "TagDB", secondary=association_table, back_populates="passwords"
    )
