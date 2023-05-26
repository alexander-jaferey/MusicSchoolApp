### imports
import json

from functools import wraps
from jose import jwt, ExpiredSignatureError
from flask import request, _request_ctx_stack
from urllib.request import urlopen

from config import auth0_domain, api_audience

### config

algorithms = ["RS256"]


### auth error exception handler


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


### auth header handlers

#### get token from request auth header


def get_token():
    auth_header = request.headers.get("Authorization", None)

    # check for existence of auth header
    if not auth_header:
        raise AuthError(
            {"description": "Authorization header should not be empty"}, 401
        )

    # split header into separate strings
    header_parts = auth_header.split()

    # check for "bearer" keyword
    if header_parts[0].lower() != "bearer":
        raise AuthError({"description": "Bearer token expected"}, 401)

    # ensure that token after "bearer" is a single string
    elif len(header_parts) != 2:
        raise AuthError({"description": "Header improperly formatted"}, 401)

    token = header_parts[1]
    return token


#### decode jwt and verify it with auth0


def check_jwt(token):
    # get jwks from auth0
    jwks_url = urlopen(f"https://{auth0_domain}/.well-known/jwks.json")
    jwks = json.loads(jwks_url.read())

    # decode auth header from request
    decoded_header = jwt.get_unverified_header(token)

    rsa_key = {}

    # check for key id in header
    if "kid" not in decoded_header:
        raise AuthError({"description": "invalid token"}, 401)

    # check header key id against auth0 jwks
    for key in jwks["keys"]:
        if key["kid"] == decoded_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=algorithms,
                audience=api_audience,
                issuer=f"https://{auth0_domain}/",
            )
            return payload

        except ExpiredSignatureError:
            raise AuthError({"description": "expired token"}, 401)

        except:
            raise AuthError({"description": "couldn't process token"}, 400)

    raise AuthError({"description": "key match error"}, 401)


#### check jwt permissions


def check_permissions(permission, payload):
    # check for permissions key in jwt
    if "permissions" not in payload:
        raise AuthError({"description": "permissions missing from token"}, 400)

    # check required permission against jwt
    elif permission not in payload["permissions"]:
        raise AuthError(
            {"description": "you don't have permission for this action"}, 403
        )

    return True


#### wrapper function to check authorization


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token()
            try:
                payload = check_jwt(token)
            except:
                raise AuthError(
                    {"description": "unable to authenticate"},
                    401
                )
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
