from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from db.database import Base


import enum
from sqlalchemy import Enum


class ModelType(enum.Enum):
    image_detection = "regression"
    image_classification = "classification"
    text_classification = "text_classification"


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    description = Column(String)
    model_type = Column(Enum(ModelType), nullable=False)

    model_versions = relationship("ModelVersion", backref="model", lazy="selectin")
    owner_id = Column(Integer, ForeignKey("users.id"))


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, index=True, unique=True)
    description = Column(String)
    endpoint_id = Column(String, unique=True)

    model_id = Column(Integer, ForeignKey("models.id"))
