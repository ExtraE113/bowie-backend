import square_client
import google_square_integration_utils


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

	if id_token is None:
		return "error: no token supplied"
	else:
		return square_client.donate(
			google_square_integration_utils.get_square_customer_from_id_token(id_token)
		)


def add_cof(request):
	# todo idempotency
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

	return square_client.store_card_on_file(nonce=nonce,
											customer=google_square_integration_utils.get_square_customer_from_id_token(
												id_token)
											)


def store_square_customer_id(request):
	# todo idempotency
	id_token = None
	request_json = request.get_json()
	if request.args and 'token' in request.args:
		id_token = request.args.get('token')
	elif request_json and 'token' in request_json:
		id_token = request_json['token']

	if id_token is None:
		return "error: no token supplied"

	square_customer_id = None
	if request.args and 'square_customer_id' in request.args:
		square_customer_id = request.args.get('square_customer_id')
	elif request_json and 'square_customer_id' in request_json:
		square_customer_id = request_json['square_customer_id']

	if square_customer_id is None:
		return "error: no square_customer_id supplied"

	return google_square_integration_utils.update_square_customer_id_by_id_token(id_token=id_token,
																				 new_square_customer_id=square_customer_id)


# class Request:
# 	@staticmethod
# 	def get_json():
# 		return {
# 			"token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjdkNTU0ZjBjMTJjNjQ3MGZiMTg1MmY3OWRiZjY0ZjhjODQzYmIxZDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZG9uYXRpb24tYXBwLTI4MTQyMCIsImF1ZCI6ImRvbmF0aW9uLWFwcC0yODE0MjAiLCJhdXRoX3RpbWUiOjE1OTMxNTYwMDMsInVzZXJfaWQiOiJHWTQ1b0M1dUNhaDZ1UlQ0NjNObm9Qam9FbWMyIiwic3ViIjoiR1k0NW9DNXVDYWg2dVJUNDYzTm5vUGpvRW1jMiIsImlhdCI6MTU5MzI4NDg1MiwiZXhwIjoxNTkzMjg4NDUyLCJlbWFpbCI6ImV6cmFAbWFubWFucy5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZXpyYUBtYW5tYW5zLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.e8qXAYklSqKQlvaAqyvkCbyV_QyPfFnU_FFXiMZedsgpzX0Pz6xq820-uxmX7n6moDpLLblvxeRmM9ba-GmLzGjjPWxhVCNhQ2QSYfj0_FjutFBSEffXqg9hcFoUjMTGOn3U8U3qzyCocTt9wmwU5_L4oadO1Prnw2Ufnt5lZv21n5Pf3aexruhqFZjG-M26icU5kvgM-mFQTzOqnJIFgczHoB_LgLVtTk9OLgQp2bKMvJddRw8_D-MLFBF6UvANtNp590rtr-f-x0a3DFKfXY2EVq884ivyXqXUCcb2J5ZJMAJ_1xBJORAGc5-Hrfw0SR0CDpYLJhDeoCQWKtxsCg",
# 			"nonce": "cnon:CBASEF33gYY9ZJl7Elk13tLlz_w",
# 			"square_customer_id": "hello"}
#
# 	args = False

def create_customer(request):
	# todo idempotency
	id_token = None
	request_json = request.get_json()
	if request.args and 'token' in request.args:
		id_token = request.args.get('token')
	elif request_json and 'token' in request_json:
		id_token = request_json['token']

	if id_token is None:
		return "error: no token supplied"

	return square_client.create_customer(email_address=google_square_integration_utils.get_user_from_id_token(id_token).email)