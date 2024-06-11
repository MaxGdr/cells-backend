from sqlalchemy import Column, ForeignKey, Integer, String

from db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, unique=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
