from typing import Annotated
from fastapi import APIRouter, File, UploadFile

from core.deps import CurrentUser, DBSessionDep
from core.config import settings
from clients.vertex import VertexAiClient
from managers.model_versions import ModelVersionsManager
from schemas.models import ModelVersionSchema
from schemas.predicts import PredictSchema

router = APIRouter()
vertex_ai_client = VertexAiClient(gcp_project_id=settings.GCP_PROJECT_ID)


@router.post("/", response_model=PredictSchema)
async def predict(
    session: DBSessionDep,
    current_user: CurrentUser,
    image: Annotated[UploadFile, File(description="A file read as UploadFile")],
    model_id: int,
    model_version: int,
) -> PredictSchema:
    """
    Create a prediction based on the image and the model version.
    """
    # Reads the file content
    image_bytes = await image.read()

    # Calls model versions models to get the model version
    model_version_schema: ModelVersionSchema = await ModelVersionsManager(
        session=session
    ).get_model_version_by_number(
        user_id=current_user.id, model_id=model_id, model_version_number=model_version
    )

    # Calls the Vertex AI client to get the predictions based on model version
    prediction: dict = vertex_ai_client.predict_image_classification(
        file_content=image_bytes,
        endpoint_id=model_version_schema.endpoint_id,
    )

    return PredictSchema._from_dict(
        predict_dict=prediction, model_version=model_version
    )
