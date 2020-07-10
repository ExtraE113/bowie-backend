import firebase_admin
import firebase_admin.auth
import firebase_admin.firestore
from google.cloud.firestore_v1 import DocumentReference

import square_client

import secret

app = firebase_admin.initialize_app(credential=secret.google_credential())
client = firebase_admin.firestore.client()


def _get_uid_from_id_token(id_token: str):
	decoded_token = firebase_admin.auth.verify_id_token(id_token, check_revoked=True)
	return decoded_token['uid']


def _get_square_customer_id_from_uid(uid: str):
	doc_ref: DocumentReference = client.document(f'user-secrets/{uid}')
	try:
		return doc_ref.get().to_dict()["square_customer_id"]
	except:
		print("howdy")
		return None


def get_square_customer_id_from_id_token(id_token: str):
	uid: str = _get_uid_from_id_token(id_token)
	return _get_square_customer_id_from_uid(uid)


def get_square_customer_from_id_token(id_token: str):
	square_customer_id = get_square_customer_id_from_id_token(id_token)
	return square_client.get_square_customer_by_id(square_customer_id)


def _update_square_customer_id_by_uid(uid: str, new_square_customer_id):
	print("here2")
	doc_ref: DocumentReference = client.document(f'users/{uid}')
	print("here3")
	result = doc_ref.set(document_data={'square_customer_id': new_square_customer_id}, merge=True)
	print("here4")
	return result


def update_square_customer_id_by_id_token(id_token: str, new_square_customer_id):
	print("here1")
	uid: str = _get_uid_from_id_token(id_token)
	print("here1.1")
	return _update_square_customer_id_by_uid(uid=uid, new_square_customer_id=new_square_customer_id)


def _get_user_from_uid(uid: str):
	return firebase_admin.auth.get_user(uid)


def get_user_from_id_token(id_token: str):
	uid = _get_uid_from_id_token(id_token)
	return _get_user_from_uid(uid)


def _update_has_cof_by_uid(uid: str, has_cof: bool = True):
	doc_ref: DocumentReference = client.document(f'users/{uid}')
	result = doc_ref.set(document_data={'has_cof': has_cof}, merge=True)
	return result


def update_has_cof_by_id_token(id_token: str, has_cof: bool = True):
	uid: str = _get_uid_from_id_token(id_token)
	_update_has_cof_by_uid(uid, has_cof)
