from sqlalchemy import Column, Integer, String
from app.config.db1 import Base
from sqlalchemy.orm import relationship


class CategoryDB(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45))
    slug = Column(String(45))

    passwords = relationship("PasswordDB", back_populates="category")
