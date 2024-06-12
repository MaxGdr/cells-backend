from typing import List, Sequence
from sqlalchemy import and_, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.models import Model


class ModelsCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_models(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Model]:
        models: Sequence[Model] = (
            self._db.scalars(
                select(Model).where(Model.owner_id == user_id).offset(skip).limit(limit)
            )
        ).all()
        return list(models)

    async def get_model(self, model_id: int, user_id: int) -> Model | None:
        model: Model | None = (
            self._db.scalars(
                select(Model).where(
                    and_(Model.owner_id == user_id, Model.id == model_id)
                )
            )
        ).one_or_none()
        return model

    async def update_model(self, model: Model, user_id: int) -> Model:
        dto_model: Model = (
            self._db.scalars(
                update(Model)
                .where(and_(Model.owner_id == user_id, Model.id == model.id))
                .values(name=model.name, description=model.description)
                .returning(Model)
            )
        ).one()
        self._db.commit()
        self._db.refresh(dto_model)
        return dto_model

    async def create_model(self, model: Model) -> Model:
        try:
            self._db.add(model)
            self._db.commit()
            self._db.refresh(model)
        except IntegrityError as exc:
            self._db.rollback()
            raise exc
        return model
