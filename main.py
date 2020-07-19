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

	nonce = None
	request_json = request.get_json()
	if request.args and 'nonce' in request.args:
		id_token = request.args.get('nonce')
	elif request_json and 'nonce' in request_json:
		id_token = request_json['nonce']

	cents = None
	request_json = request.get_json()
	if request.args and 'cents' in request.args:
		cents = int(request.args.get('cents'))
	elif request_json and 'cents' in request_json:
		cents = int(request_json['cents'])

	if cents is None:
		return "error: cents is mandatory"

	if id_token is None and nonce is None:
		return "error: neither id_token nor nonce supplied"
	else:
		if id_token is not None:
			return str(square_client.donate(
				cents,
				google_square_integration_utils.get_square_customer_from_id_token(id_token)
			))
		elif nonce is not None:
			return "Donating with a nonce is not yet supported"  # todo


# hit this endpoint to store a card on file with a nonce.
# creates a square customer if the user doesn't already have one stored
# todo test- is this even working?
def add_cof(request):
	try:
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

		global customer_id

		customer_id = google_square_integration_utils.get_square_customer_id_from_id_token(id_token)
		print(customer_id)
		if customer_id is None:
			print("here")
			result = square_client.create_customer(
				email_address=google_square_integration_utils.get_user_from_id_token(id_token).email)
			print(result)
			customer_id = result["id"]
		return "got to line 88"
		square_client.store_card_on_file(nonce=nonce, customer_id=customer_id)
		return str(google_square_integration_utils.update_square_customer_id_by_id_token(id_token, customer_id))
	except BaseException as e:
		print(e)
