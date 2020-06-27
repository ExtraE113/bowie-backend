import json
from collections import namedtuple
from uuid import uuid4

from square.client import Client
import os


SQUARE_APPLICATION_TOKEN = os.getenv('SQUARE_APPLICATION_TOKEN')
assert SQUARE_APPLICATION_TOKEN is not None
client = Client(
	environment="sandbox",
	access_token=SQUARE_APPLICATION_TOKEN

)
customers_api = client.customers
payments_api = client.payments


def create_customer(given_name: str, family_name: str, email_address: str):
	if customer_already_exists(given_name=given_name, family_name=family_name, email_address=email_address):
		print("customer already exists")
	else:
		body = {'given_name': given_name, 'family_name': family_name, 'email_address': email_address}

		result = customers_api.create_customer(body)


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


def store_card_on_file(nonce: str, given_name: str = None, family_name: str = None, email_address: str = None):
	customers = get_customers(given_name=given_name, family_name=family_name, email_address=email_address).text
	customers = json.loads(customers, object_hook=lambda d: namedtuple('customers_x', d.keys())(*d.values())).customers
	print(customers)
	if len(customers) == 0:
		raise ValueError("No customer found with given params, so no card could be stored")
	if len(customers) > 1:
		raise ValueError("Something has gone wrong, as multiple customers exist with that combination of params")
	if len(customers) == 1:
		body = {'card_nonce': nonce}
		customer_id = customers[0].id
		result = customers_api.create_customer_card(customer_id, body)


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
		print(result.body)
	elif result.is_error():
		print(result.errors)


def get_square_customer_by_id(customer_id: str):
	customer = customers_api.retrieve_customer(customer_id).text
	customer = json.loads(customer, object_hook=lambda d: namedtuple('customers_x', d.keys())(*d.values()))[0]

	return customer
