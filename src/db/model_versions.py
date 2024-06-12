from typing import List, Sequence
from sqlalchemy import and_, cast, select, update
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.models import Model, ModelVersion


class ModelVersionsCrud:
    def __init__(self, db: Session):
        self._db = db

    async def get_model_versions(
        self, model_id: int, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[ModelVersion]:
        model_versions: Sequence[ModelVersion] = (
            self._db.scalars(
                select(ModelVersion)
                .join(Model)
                .where(
                    and_(
                        Model.id == model_id,
                        Model.owner_id == user_id,
                        ModelVersion.model_id == Model.id,
                    )
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
            self._db.scalars(
                select(ModelVersion)
                .join(Model)
                .where(
                    and_(
                        ModelVersion.number == cast(version, sqlalchemy.Integer),
                        ModelVersion.model_id == model_id,
                        Model.owner_id == user_id,
                    )
                )
            )
        ).one_or_none()
        return model_version

    async def update_model_version(self, model: ModelVersion) -> ModelVersion:
        model_version: ModelVersion = (
            self._db.scalars(
                update(ModelVersion)
                .where(
                    and_(
                        ModelVersion.number == model.number, ModelVersion.id == model.id
                    )
                )
                .values(
                    endpoint_id=model.endpoint_id,
                    description=model.description,
                )
                .returning(Model)
            )
        ).one()
        self._db.commit()
        self._db.refresh(model_version)
        return model_version

    async def create_model_version(self, model_version: ModelVersion) -> Model:
        try:
            self._db.add(model_version)
            self._db.commit()
            self._db.refresh(model_version)
        except IntegrityError as exc:
            self._db.rollback()
            raise exc
        return model_version
