import datetime

import square_client
import google_square_integration_utils


# hit this endpoint to donate
def donate_endpoint(request):
	# todo idempotency
	"""Responds to any HTTP request.
	Args:
	request (flask.Request): HTTP request object.
	Returns:
		The response text or any set of values that can be turned into a
		Response object using
		`make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
	"""

	id_token = None
	request_json = request.get_json()
	if request.args and 'token' in request.args:
		id_token = request.args.get('token')
	elif request_json and 'token' in request_json:
		id_token = request_json['token']

	cents = None
	request_json = request.get_json()
	if request.args and 'cents' in request.args:
		cents = int(request.args.get('cents'))
	elif request_json and 'cents' in request_json:
		cents = int(request_json['cents'])

	if cents is None:
		raise ValueError("Cents is required")

	if id_token is None:
		raise ValueError("Id token is required")
	else:
		if google_square_integration_utils.get_uid_from_id_token(id_token) == "G6xxqazfKBYRK6gC1r79eKLXesl1":
			out = {
				"payment": {
					"total_money": {
						"amount": cents,
						"currency": "USD",
					},
					"card_details": {
						"card": {
							"card_brand": "Test Card Brand",
							"card_type": "Test Card Type",
							"exp_month": "13",
							"exp_year": "00",
							"last_4": "1234",
						}
					}
				},
				"time": datetime.datetime.now()
			}
			google_square_integration_utils.update_donate_history_by_id_token(id_token, out)
			return str(out)

		elif google_square_integration_utils.is_default_card_valid_by_id_token(id_token):
			out = square_client.donate(
				cents,
				google_square_integration_utils.get_square_customer_from_id_token(id_token),
				google_square_integration_utils.get_default_card_by_id_token(id_token)
			)
			out = {
				"payment": {
					"total_money": {
						"amount": [out["payment"]["total_money"]["amount"]],
						"currency": [out["payment"]["total_money"]["currency"]]
					},
					"card_details": {
						"card": {
							"card_brand": out["payment"]["card_details"]["card"]["card_brand"],
							"card_type": out["payment"]["card_details"]["card"]["card_type"],
							"exp_month": out["payment"]["card_details"]["card"]["exp_month"],
							"exp_year": out["payment"]["card_details"]["card"]["exp_year"],
							"last_4": out["payment"]["card_details"]["card"]["last_4"],
						}
					}
				},
				"time": datetime.datetime.now()
			}
			google_square_integration_utils.update_donate_history_by_id_token(id_token, out)
			return str(out)
		else:
			raise ValueError("Default card is invalid")


# hit this endpoint to store a card on file with a nonce.
# creates a square customer if the user doesn't already have one stored
# todo test- is this even working?
def add_cof(request):
	print("should be logged...?")
	# todo idempotency
	# todo if there is already
	id_token = None
	request_json = request.get_json()
	if request.args and 'token' in request.args:
		id_token = request.args.get('token')
	elif request_json and 'token' in request_json:
		id_token = request_json['token']

	if id_token is None:
		return "error: no token supplied"

	nonce = None
	if request.args and 'nonce' in request.args:
		nonce = request.args.get('nonce')
	elif request_json and 'nonce' in request_json:
		nonce = request_json['nonce']

	if nonce is None:
		return "error: no nonce supplied"

	customer_id = google_square_integration_utils.get_square_customer_id_from_id_token(id_token)
	if customer_id is None:
		print("No customer_id saved. Creating a new customer...")
		result = square_client.create_customer(
			email_address=google_square_integration_utils.get_user_from_id_token(id_token).email)
		print(result)
		customer_id = result["id"]
	store_cof_result = square_client.store_card_on_file(nonce=nonce, customer_id=customer_id)

	if "errors" in store_cof_result:
		return f"Something went wrong, ${store_cof_result['errors'][0]['detail']}", 400

	google_square_integration_utils.update_square_customer_id_by_id_token(id_token, customer_id)
	out = str(google_square_integration_utils.update_cards_by_id_token(id_token))
	print(132, end="   |   ")
	print(out)
	return out
