from typing import List, Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from models.models import Model, ModelVersion


class ModelVersionsCrud:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_model_versions(
        self, model_id: int, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[ModelVersion]:
        model_versions: Sequence[ModelVersion] = (
            await self._db.scalars(
                select(ModelVersion)
                .join(Model)
                .where(
                    Model.id == model_id
                    and Model.owner_id == user_id
                    and ModelVersion.model_id == Model.id
                )
                .offset(skip)
                .limit(limit)
            )
        ).all()
        return list(model_versions)

    async def get_model_version_by_version(
        self, version: int, model_id: int, user_id: int
    ) -> ModelVersion:
        model_version: ModelVersion | None = (
            await self._db.scalars(
                select(ModelVersion)
                .join(Model)
                .where(
                    ModelVersion.number == version
                    and ModelVersion.model_id == model_id
                    and Model.owner_id == user_id
                )
            )
        ).one_or_none()
        return model_version

    async def update_model_version(self, model: ModelVersion) -> ModelVersion:
        model_version: ModelVersion = (
            await self._db.scalars(
                update(ModelVersion)
                .where(
                    ModelVersion.number == model.number and ModelVersion.id == model.id
                )
                .values(
                    endpoint_id=model.endpoint_id,
                    description=model.description,
                )
                .returning(Model)
            )
        ).one()
        await self._db.commit()
        await self._db.refresh(model_version)
        return model_version

    async def create_model_version(self, model_version: ModelVersion) -> Model:
        try:
            self._db.add(model_version)
            await (
                self._db.commit()
            )  # Can be placed on manager level instead to improve commit performance
            await self._db.refresh(model_version)
        except IntegrityError as exc:
            await self._db.rollback()
            raise exc
        return model_version
