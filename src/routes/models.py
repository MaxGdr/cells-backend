from typing import List

from fastapi import APIRouter

from managers.models import ModelsManager
from managers.model_versions import ModelVersionsManager


from core.deps import CurrentUser, DBSessionDep
from schemas.models import (
    ModelSchema,
    ModelVersionSchema,
    ModelVersionsCreateRequestSchema,
    ModelVersionsGetResponseSchema,
    ModelVersionsUpdateRequestSchema,
    ModelsCreateRequestSchema,
    ModelsGetResponseSchema,
    ModelsUpdateRequestSchema,
)

router = APIRouter()


@router.get("/", response_model=ModelsGetResponseSchema)
async def get_models(
    session: DBSessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> ModelsGetResponseSchema:
    """
    Retrieve items.
    """

    models: List[ModelSchema] = await ModelsManager(session=session).get_models(
        skip=skip, limit=limit, user_id=current_user.id
    )

    return ModelsGetResponseSchema(
        data=models,
        count=len(models),
    )


@router.get("/{model_id}/modelversions", response_model=ModelVersionsGetResponseSchema)
async def get_model_versions(
    session: DBSessionDep,
    current_user: CurrentUser,
    model_id: int,
    skip: int = 0,
    limit: int = 100,
) -> ModelVersionsGetResponseSchema:
    """
    Retrieve items.
    """

    model_versions: List[ModelVersionSchema] = await ModelVersionsManager(
        session=session
    ).get_model_versions(
        model_id=model_id, skip=skip, limit=limit, user_id=current_user.id
    )

    return ModelVersionsGetResponseSchema(
        data=model_versions,
        count=len(model_versions),
    )


@router.get("/{model_id}", response_model=ModelSchema)
async def get_model(
    session: DBSessionDep,
    current_user: CurrentUser,
    model_id: int,
) -> ModelSchema:
    """
    Create an item.
    """

    model: ModelSchema = await ModelsManager(session=session).get_model(
        user_id=current_user.id, model_id=model_id
    )
    return model


@router.get(
    "/{model_id}/modelversions/{model_version}", response_model=ModelVersionSchema
)
async def get_model_version(
    session: DBSessionDep,
    current_user: CurrentUser,
    model_id: int,
    model_version: int,
) -> ModelVersionSchema:
    """
    Create an item.
    """

    new_model_version: ModelVersionSchema = await ModelVersionsManager(
        session=session
    ).get_model_version_by_number(
        user_id=current_user.id, model_id=model_id, model_version_number=model_version
    )
    return new_model_version


@router.put("/{model_id}", response_model=ModelSchema)
async def update_model(
    session: DBSessionDep,
    current_user: CurrentUser,
    model_request: ModelsUpdateRequestSchema,
    model_id: int,
) -> ModelSchema:
    """
    Create an item.
    """

    model: ModelSchema = await ModelsManager(session=session).update_model(
        model_request=ModelSchema(
            id=model_id,
            name=model_request.name,
            description=model_request.description,
            owner_id=current_user.id,
        )
    )
    return model


@router.put(
    "/{model_id}/modelversions/{model_version}", response_model=ModelVersionSchema
)
async def update_model_version(
    session: DBSessionDep,
    current_user: CurrentUser,
    model_version_request: ModelVersionsUpdateRequestSchema,
    model_version: int,
    model_id: int,
) -> ModelVersionSchema:
    """
    Create an item.
    """

    new_model_version: ModelVersionSchema = await ModelVersionsManager(
        session=session
    ).update_model_version(
        model_version_request=ModelVersionSchema(
            number=model_version,
            endpoint_id=model_version_request.endpoint_id,
            description=model_version_request.description,
            model_id=model_id,
        ),
        user_id=current_user.id,
    )
    return new_model_version


@router.post("/", response_model=ModelSchema)
async def create_model(
    session: DBSessionDep,
    current_user: CurrentUser,
    model_request: ModelsCreateRequestSchema,
) -> ModelSchema:
    """
    Create an item.
    """

    model: ModelSchema = await ModelsManager(session=session).create(
        model=ModelSchema(
            name=model_request.name,
            description=model_request.description,
            model_type=model_request.model_type,
            owner_id=current_user.id,
        )
    )
    return model


@router.post("/{model_id}/modelversions", response_model=ModelVersionSchema)
async def create_model_version(
    session: DBSessionDep,
    current_user: CurrentUser,
    model_id: int,
    model_version_request: ModelVersionsCreateRequestSchema,
) -> ModelVersionSchema:
    """
    Create an item.
    """

    model_version: ModelVersionSchema = await ModelVersionsManager(
        session=session
    ).create(
        model_id=model_id,
        endpoint_id=model_version_request.endpoint_id,
        description=model_version_request.description,
        user_id=current_user.id,
    )
    return model_version
