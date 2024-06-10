from typing import List, Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from models.models import Model


class ModelsCrud:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_models(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Model]:
        models: Sequence[Model] = (
            await self._db.scalars(
                select(Model).where(Model.owner_id == user_id).offset(skip).limit(limit)
            )
        ).all()
        return list(models)

    async def get_model(self, model_id: int, user_id: int) -> Model | None:
        model: Model | None = (
            await self._db.scalars(
                select(Model).where(Model.owner_id == user_id and Model.id == model_id)
            )
        ).one_or_none()
        return model

    async def update_model(self, model: Model, user_id: int) -> Model:
        model: Model = (
            await self._db.scalars(
                update(Model)
                .where(Model.owner_id == user_id and Model.id == model.id)
                .values(name=model.name, description=model.description)
                .returning(Model)
            )
        ).one()
        await self._db.commit()
        await self._db.refresh(model)
        return model

    async def create_model(self, model: Model) -> Model:
        try:
            self._db.add(model)
            await (
                self._db.commit()
            )  # Can be placed on manager level instead to improve commit performance
            await self._db.refresh(model)
        except IntegrityError as exc:
            await self._db.rollback()
            raise exc
        return model
