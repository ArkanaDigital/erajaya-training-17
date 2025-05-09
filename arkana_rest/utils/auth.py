import json
from functools import wraps
from werkzeug.exceptions import Unauthorized

from odoo.http import request, Response

def token_auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            auth_header = request.httprequest.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return json_response({"error": "Missing or invalid Authorization header"}, 401)

            token = auth_header.split(" ")[1]

            # Use Odoo 17's API key system instead of _authenticate_bearer_token
            try:
                uid = request.env['res.users.apikeys']._check_credentials(scope='rpc', key=token)
                if not uid:
                    return json_response({"error": "Invalid or expired token"}, 401)

                # Updated: Use request.update_env instead of directly setting request.uid
                request.update_env(user=uid)
            except Exception as e:
                return json_response({"error": f"Authentication error: {str(e)}"}, 401)

            return func(*args, **kwargs)
        except Exception as e:
            return json_response({"error": f"General error: {str(e)}"}, 500)

    return wrapper

def json_response(data, status=200):
    """Helper function to create proper JSON responses"""
    body = json.dumps(data)
    headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(body)))
    ]
    return Response(body, status=status, headers=headers)
