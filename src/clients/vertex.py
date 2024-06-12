from typing import Any
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.cloud.aiplatform_v1.types import prediction_service
import logging
import base64
import time


class VertexAiClient:
    def __init__(self, gcp_project_id: str):
        self._logger = logging.getLogger(__name__)
        self._gcp_project_id = gcp_project_id

    def predict_image_classification(
        self,
        file_content: bytes,
        endpoint_id: str,
        location: str = "europe-west4",
        api_endpoint: str = "europe-west4-aiplatform.googleapis.com",
    ) -> dict[str, Any]:
        # The AI Platform services require regional API endpoints.
        client_options = {"api_endpoint": api_endpoint}
        # Initialize client that will be used to create and send requests.
        # This client only needs to be created once, and can be reused for multiple requests.
        client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

        # The format of each instance should conform to the deployed model's prediction input schema.
        encoded_content = base64.b64encode(file_content).decode(encoding="utf-8")
        instance = predict.instance.ImageClassificationPredictionInstance(
            content=encoded_content,
        ).to_value()
        instances = [instance]

        # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
        parameters = predict.params.ImageClassificationPredictionParams(
            confidence_threshold=0.5,
            max_predictions=5,
        ).to_value()

        endpoint = client.endpoint_path(
            project=self._gcp_project_id, location=location, endpoint=endpoint_id
        )
        # Log how long predict method is taking
        self._logger.info("Sending prediction request")
        start_time = time.time()

        # Perform the prediction
        response: prediction_service.PredictResponse = client.predict(
            endpoint=endpoint, instances=instances, parameters=parameters
        )

        end_time = time.time()
        delta_time = end_time - start_time

        self._logger.info("Prediction took %s seconds", delta_time)
        formatted_predictions = [
            dict(prediction) for prediction in response.predictions
        ]
        return formatted_predictions[0]
