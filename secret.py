import json
import os

from firebase_admin.credentials import Certificate
from google.cloud import secretmanager

if os.getenv("BOWIE_BACKEND_DEBUG") is None:  # ie if the env var isn't set
	client = secretmanager.SecretManagerServiceClient()
	project_id = os.environ["GCP_PROJECT"]

	square_secret = "square_application_token"
	square_resource_name = f"projects/{project_id}/secrets/{square_secret}/versions/latest"
	response = client.access_secret_version(square_resource_name)
	square_secret_string = response.payload.data.decode('UTF-8')

	google_secret = "firebase_admin_sdk"
	google_resource_name = f"projects/{project_id}/secrets/{google_secret}/versions/latest"
	response = client.access_secret_version(google_resource_name)
	google_secret_string = response.payload.data.decode('UTF-8')
	google_secret_dict: str = json.loads(google_secret_string)


def square_application_token():
	if os.getenv("BOWIE_BACKEND_DEBUG") is not None:
		return os.getenv("SQUARE_APPLICATION_TOKEN")
	return square_secret_string


def google_credential():
	if os.getenv("BOWIE_BACKEND_DEBUG") is not None:
		return None
	return Certificate(google_secret_dict)
