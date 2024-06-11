from typing import List
from pydantic import BaseModel, ConfigDict
from models.models import ModelType, Model, ModelVersion


class ModelVersionSchema(BaseModel):
    id: int | None = None
    number: int
    description: str | None = None
    endpoint_id: str
    model_id: int

    model_config = ConfigDict(protected_namespaces=())

    @staticmethod
    def _from_dto(model_version: ModelVersion):  # type: ignore
        return ModelVersionSchema(
            id=model_version.id,
            number=model_version.number,
            description=model_version.description,
            endpoint_id=model_version.endpoint_id,
            model_id=model_version.model_id,
        )

    def _to_dto(self) -> ModelVersion:
        return ModelVersion(
            id=self.id,
            number=self.number,
            description=self.description,
            endpoint_id=self.endpoint_id,
            model_id=self.model_id,
        )


class ModelSchema(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    model_type: ModelType | None = None

    model_versions: List[ModelVersionSchema] = []
    owner_id: int

    model_config = ConfigDict(protected_namespaces=())

    @staticmethod
    def _from_dto(model: Model):  # type: ignore
        return ModelSchema(
            id=model.id,
            name=model.name,
            owner_id=model.owner_id,
            description=model.description,
            model_type=model.model_type,
            model_versions=[
                ModelVersionSchema._from_dto(model_version)
                for model_version in model.model_versions
            ],
        )

    def _to_dto(self) -> Model:
        return Model(
            id=self.id,
            name=self.name,
            description=self.description,
            model_type=self.model_type,
            model_versions=self.model_versions,
            owner_id=self.owner_id,
        )


class ModelsGetResponseSchema(BaseModel):
    data: List[ModelSchema]
    count: int


class ModelsCreateRequestSchema(BaseModel):
    name: str
    description: str | None = None
    model_type: ModelType | None = None

    model_config = ConfigDict(protected_namespaces=())


class ModelsUpdateRequestSchema(BaseModel):
    name: str
    description: str | None = None


class ModelVersionsGetResponseSchema(BaseModel):
    data: List[ModelVersionSchema]
    count: int


class ModelVersionsUpdateRequestSchema(BaseModel):
    description: str | None = None
    endpoint_id: str


class ModelVersionsCreateRequestSchema(BaseModel):
    description: str | None = None
    endpoint_id: str
