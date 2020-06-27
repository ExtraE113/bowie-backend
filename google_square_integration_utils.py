import firebase_admin
import firebase_admin.auth
import firebase_admin.firestore
from google.cloud.firestore_v1 import DocumentReference

app = firebase_admin.initialize_app()


def get_uid_from_id_token(id_token: str):
	decoded_token = firebase_admin.auth.verify_id_token(id_token)
	return decoded_token['uid']


def get_square_customer_id_from_uid(uid: str):
	client = firebase_admin.firestore.client()
	doc_ref: DocumentReference = client.document(f'users/{uid}')
	return doc_ref.get().to_dict()["square_customer_id"]


def get_square_customer_id_from_id_token(id_token: str):
	uid: str = get_uid_from_id_token(id_token)
	return get_square_customer_id_from_uid(uid)
