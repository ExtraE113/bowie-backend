import json
from collections import namedtuple
from uuid import uuid4
import secret

from square.client import Client

SQUARE_APPLICATION_TOKEN = secret.square_application_token()
assert SQUARE_APPLICATION_TOKEN is not None
client = Client(
	environment="sandbox",
	access_token=SQUARE_APPLICATION_TOKEN

)
customers_api = client.customers
payments_api = client.payments


def create_customer(given_name: str = None, family_name: str = None, email_address: str = None):
	# todo check if customer already exists
	body = {'email_address': email_address}
	result = customers_api.create_customer(body).body
	return result["customer"]


# doesn't work fixme
def customer_already_exists(given_name: str = None, family_name: str = None, email_address: str = None):
	existing_customers = get_customers(given_name=given_name, family_name=family_name, email_address=email_address)
	return existing_customers == {}


def get_customers(given_name: str = None, family_name: str = None, email_address: str = None):
	if not (given_name is not None and family_name is not None and email_address is not None):
		raise ValueError("must provide given_name, family_name, and email_address")

	body = {'limit': 1, 'given_name': given_name, 'family_name': family_name, 'email_address': email_address}
	existing_customers = customers_api.search_customers(body)
	return existing_customers


def store_card_on_file(nonce: str, customer_id):
	body = {'card_nonce': nonce}
	result = customers_api.create_customer_card(customer_id, body).body
	return result


def donate(customer=None):
	body = dict()

	body['source_id'] = customer.cards[0][0]
	body['idempotency_key'] = str(uuid4())[:44]
	body['amount_money'] = {}
	body['amount_money']['amount'] = 200
	body['amount_money']['currency'] = 'USD'
	body['autocomplete'] = True
	body['customer_id'] = customer.id

	result = payments_api.create_payment(body)

	if result.is_success():
		return result.body
	elif result.is_error():
		return result.errors


def get_square_customer_by_id(customer_id: str):
	customer = customers_api.retrieve_customer(customer_id).text  # todo what if I do .body instea of .text? do I still need the blackmagic below?
	customer = json.loads(customer, object_hook=lambda d: namedtuple('customers_x', d.keys())(*d.values()))[0][0]
	return customer
