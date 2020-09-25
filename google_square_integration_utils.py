import firebase_admin
import firebase_admin.auth
import firebase_admin.firestore
from firebase_admin import firestore
from google.cloud.firestore_v1 import DocumentReference

import square_client

import secret

app = firebase_admin.initialize_app(credential=secret.google_credential())
client = firebase_admin.firestore.client()


def get_uid_from_id_token(id_token: str):
	decoded_token = firebase_admin.auth.verify_id_token(id_token, check_revoked=True)
	return decoded_token['uid']


def _get_square_customer_id_from_uid(uid: str):
	doc_ref: DocumentReference = client.document(f'user-secrets/{uid}')
	try:
		return doc_ref.get().to_dict()["square_customer_id"]
	except:
		print("No square customer with given uid")
		return None


def get_square_customer_id_from_id_token(id_token: str):
	uid: str = get_uid_from_id_token(id_token)
	return _get_square_customer_id_from_uid(uid)


def get_square_customer_from_id_token(id_token: str):
	square_customer_id = get_square_customer_id_from_id_token(id_token)
	return square_client.get_square_customer_by_id(square_customer_id)


def _update_square_customer_id_by_uid(uid: str, new_square_customer_id):
	secret_doc_ref: DocumentReference = client.document(f'user-secrets/{uid}')
	secret_result = secret_doc_ref.set(document_data={'square_customer_id': new_square_customer_id}, merge=True)
	doc_ref: DocumentReference = client.document(f"user-readonly/{uid}")
	result = doc_ref.set(document_data={"has_cof": True}, merge=True)
	return result


def update_square_customer_id_by_id_token(id_token: str, new_square_customer_id):
	uid: str = get_uid_from_id_token(id_token)
	return _update_square_customer_id_by_uid(uid=uid, new_square_customer_id=new_square_customer_id)


def _get_user_from_uid(uid: str):
	return firebase_admin.auth.get_user(uid)


def get_user_from_id_token(id_token: str):
	uid = get_uid_from_id_token(id_token)
	return _get_user_from_uid(uid)


def _update_cards_by_uid(uid: str):
	doc_ref: DocumentReference = client.document(f"user-readonly/{uid}")
	# todo lots of this should be cashed
	customer_id = _get_square_customer_id_from_uid(uid)
	customer = square_client.get_square_customer_by_id(customer_id)
	cards = customer.cards
	cards_serilized = [
		{"card_brand": card.card_brand, "last_4": card.last_4, "exp_month": card.exp_month, "exp_year": card.exp_year,
			"id": card.id}
		for card in cards]
	result = doc_ref.set(document_data={"cards": cards_serilized}, merge=True)
	return result


def update_cards_by_id_token(id_token: str):
	uid: str = get_uid_from_id_token(id_token)
	return _update_cards_by_uid(uid)


def _update_donate_history_by_uid(uid: str, transaction_info: dict):
	doc_ref: DocumentReference = client.document(f"user-readonly/{uid}")
	trans = client.transaction()

	@firestore.firestore.transactional
	def update_in_transaction(t, dr):
		snapshot = dr.get(transaction=t)
		try:
			history = snapshot.get("history")
		except KeyError:
			history = []
		history.append(transaction_info)
		t.set(dr, {
			'history': history
		}, merge=True)

	update_in_transaction(trans, doc_ref)


def update_donate_history_by_id_token(id_token: str, transaction_info: dict):
	uid: str = get_uid_from_id_token(id_token)
	return _update_donate_history_by_uid(uid, transaction_info)


def _get_default_card_by_uid(uid: str):
	doc_ref: DocumentReference = client.document(f'users/{uid}')
	default: str
	try:
		default = doc_ref.get().to_dict()["default_card"]
	except KeyError:
		doc_ref = client.document(f'user-readonly/{uid}')
		default = doc_ref.get().to_dict()["cards"][0]["id"]

	return default


def get_default_card_by_id_token(id_token: str):
	uid: str = get_uid_from_id_token(id_token)
	return _get_default_card_by_uid(uid)


def _is_default_card_valid_by_uid(uid: str):
	customer_id = _get_square_customer_id_from_uid(uid)
	customer = square_client.get_square_customer_by_id(customer_id)
	cards = customer.cards
	default = _get_default_card_by_uid(uid)

	for i in cards:
		if i.id == default:
			return True
	return False


def is_default_card_valid_by_id_token(id_token: str):
	uid: str = get_uid_from_id_token(id_token)
	return _is_default_card_valid_by_uid(uid)
