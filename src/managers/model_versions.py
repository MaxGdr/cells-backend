from typing import List

from fastapi import HTTPException
from db.model_versions import ModelVersionsCrud
from db.models import ModelsCrud
from models.models import Model, ModelVersion
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from schemas.models import ModelVersionSchema


class ModelVersionsManager:
    def __init__(self, session: AsyncSession):
        self._model_versions_crud = ModelVersionsCrud(db=session)
        self._model_crud = ModelsCrud(db=session)

    async def get_model_versions(
        self, model_id: int, user_id: int, skip: int, limit: int
    ) -> List[ModelVersionSchema]:
        model_versions: List[
            ModelVersion
        ] = await self._model_versions_crud.get_model_versions(
            model_id=model_id, user_id=user_id, skip=skip, limit=limit
        )
        return [
            ModelVersionSchema._from_dto(model_version=version)
            for version in model_versions
        ]

    async def get_model_version_by_number(
        self, model_version_number: int, model_id: int, user_id: int
    ) -> ModelVersionSchema:
        model_version: (
            ModelVersion | None
        ) = await self._model_versions_crud.get_model_version_by_version(
            model_version_number=model_version_number,
            model_id=model_id,
            user_id=user_id,
        )
        if not model_version:
            raise HTTPException(status_code=404, detail="Model Version not found")
        return ModelVersionSchema._from_dto(model=model_version)

    async def update_model_version(
        self, model_version_request: ModelVersionSchema, user_id: int
    ) -> ModelVersionSchema:
        db_model_version: (
            ModelVersion | None
        ) = await self._model_versions_crud.get_model_version_by_version(
            version=model_version_request.number,
            user_id=user_id,
            model_id=model_version_request.id,
        )
        db_model: Model | None = await self._model_crud.get_model(
            model_id=model_version_request.model_id, user_id=user_id
        )
        if not db_model:
            raise HTTPException(status_code=404, detail="Model not found")

        if not db_model_version:
            raise HTTPException(status_code=404, detail="Model Version not found")

        if db_model.owner_id != user_id:
            raise HTTPException(
                status_code=403, detail="Forbidden. User is not the owner of the model."
            )

        db_model_version.endpoint_id = model_version_request.endpoint_id
        db_model_version.description = model_version_request.description

        updated_model_version = await self._model_versions_crud.update_model_version(
            model_version=db_model_version
        )
        return ModelVersionSchema._from_dto(model=updated_model_version)

    async def create(
        self, model_id: str, endpoint_id: str, description: str, user_id: int
    ) -> ModelVersionSchema:
        db_model: Model | None = await self._model_crud.get_model(
            model_id=model_id, user_id=user_id
        )

        if not db_model:
            raise HTTPException(status_code=404, detail="Model not found")

        # Get the next model version number
        if not db_model.model_versions:
            model_version_number = 1
        else:
            model_version_number = (
                max([int(version.number) for version in db_model.model_versions]) + 1
            )

        try:
            db_model_version: Model = (
                await self._model_versions_crud.create_model_version(
                    model_version=ModelVersion(
                        number=model_version_number,
                        description=description,
                        endpoint_id=endpoint_id,
                        model_id=model_id,
                    )
                )
            )
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Bad request.")
        return ModelVersionSchema._from_dto(model_version=db_model_version)
