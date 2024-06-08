from sqlalchemy import Column, Integer, String, DateTime, Boolean

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    email = Column("email", String, index=True, unique=True)
    password = Column("password", String, nullable=False)
    is_active = Column("is_active", Boolean, nullable=False)
    created_at = Column("created_at", DateTime, nullable=False)
    updated_at = Column("updated_at", DateTime, nullable=True)
    full_name = Column("full_name", String, nullable=False)
