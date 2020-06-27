from square_client import donate
from square_client import get_square_customer_by_id
from google_square_integration_utils import get_square_customer_id_from_id_token


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
	if request.args and 'message' in request.args:
		id_token = request.args.get('token')
	elif request_json and 'message' in request_json:
		id_token = request_json['token']

	if id_token is None:
		return "error: no token supplied"
	else:
		donate(
			get_square_customer_by_id(
				get_square_customer_id_from_id_token(id_token)
			)
		)