import json
import os
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
project_id = os.environ["GCP_PROJECT"]

square_secret = "square_application_token"
square_resource_name = f"projects/{project_id}/secrets/{square_secret}/versions/latest"
response = client.access_secret_version(square_resource_name)
square_secret_string = response.payload.data.decode('UTF-8')

google_secret = "square_application_token"
google_resource_name = f"projects/{project_id}/secrets/{google_secret}/versions/latest"
response = client.access_secret_version(google_resource_name)
google_secret_string = response.payload.data.decode('UTF-8')
google_secret_dict: str = json.loads(google_secret_string)


def square_application_token():
    return square_secret_string


def google_credential():
    return google_secret_dict
