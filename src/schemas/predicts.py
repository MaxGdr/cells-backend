from pydantic import BaseModel, ConfigDict
from models.models import ModelVersion
from schemas.models import ModelVersionSchema


class PredictSchema(BaseModel):
    confidences: float
    predicted_class: str
    model_version: ModelVersionSchema

    model_config = ConfigDict(protected_namespaces=())

    @staticmethod
    def _from_dict(predict_dict: dict, model_version: ModelVersion):  # type: ignore
        return PredictSchema(
            confidences=predict_dict["confidences"][0],
            predicted_class=predict_dict["displayNames"][0],
            model_version=model_version,
        )
