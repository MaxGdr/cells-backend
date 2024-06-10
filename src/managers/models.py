from typing import List

from fastapi import HTTPException
from db.models import ModelsCrud
from models.models import Model
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from schemas.models import ModelSchema


class ModelsManager:
    def __init__(self, session: AsyncSession):
        self._models_crud = ModelsCrud(db=session)

    async def get_models(
        self, skip: int, limit: int, user_id: int
    ) -> List[ModelSchema]:
        models: List[Model] = await self._models_crud.get_models(
            user_id=user_id, skip=skip, limit=limit
        )
        return [ModelSchema._from_dto(model=model) for model in models]

    async def get_model(self, model_id: int, user_id: int) -> ModelSchema:
        model: Model | None = await self._models_crud.get_model(
            user_id=user_id, model_id=model_id
        )
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        return ModelSchema._from_dto(model=model)

    async def update_model(self, model_request: ModelSchema) -> ModelSchema:
        db_model: Model | None = await self._models_crud.get_model(
            user_id=model_request.owner_id, model_id=model_request.id
        )
        if not db_model:
            raise HTTPException(status_code=404, detail="Model not found")

        if model_request.owner_id != db_model.owner_id:
            raise HTTPException(
                status_code=403, detail="Forbidden. User is not the owner of the model."
            )

        db_model.name = model_request.name
        db_model.description = model_request.description

        updated_model = await self._models_crud.update_model(
            model=db_model, user_id=db_model.owner_id
        )
        return ModelSchema._from_dto(model=updated_model)

    async def create(self, model: ModelSchema) -> ModelSchema:
        try:
            db_model: Model = await self._models_crud.create_model(
                model=Model(
                    name=model.name,
                    description=model.description,
                    owner_id=model.owner_id,
                    model_type=model.model_type,
                )
            )
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User owner id is not valid")
        return ModelSchema._from_dto(model=db_model)
