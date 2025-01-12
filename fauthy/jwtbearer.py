"""Module providing a secure JWT bearer token dependency for FastAPI."""

import json
import os

import jwt
import requests
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import algorithms
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


def get_jwks():
    """
    Get the JWKS from the JWKS_URL environment variable.
    This is extracted as a single function to make it easier to mock in tests.
    """
    return requests.get(os.environ["JWKS_URL"], timeout=10).json()


class JWTBearer(HTTPBearer):
    """JWT bearer token dependency for FastAPI."""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    def get_public_key(self, kid: str) -> dict:
        """Get the public key from the JWKS."""
        jwks = get_jwks()
        for key in jwks["keys"]:
            if key["kid"] == kid:
                return key
        return None

    def verify_jwk_token(self, credentials: HTTPAuthorizationCredentials) -> dict:
        """Verify the JWT token using the JWK."""
        unverified_header = jwt.get_unverified_header(credentials)
        public_key = self.get_public_key(unverified_header["kid"])
        if public_key is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="JWK public key not found"
            )
        try:
            public_key_encoded = algorithms.RSAAlgorithm.from_jwk(
                json.dumps(public_key)
            )
            payload = jwt.decode(
                credentials,
                key=public_key_encoded,
                algorithms=[
                    unverified_header["alg"],
                ],
                audience=os.environ["AUDIENCE"],
                issuer=os.environ["ISSUER"],
            )
            return payload
        except jwt.ExpiredSignatureError as exc:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Token expired"
            ) from exc
        except jwt.InvalidAudienceError as exc:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Invalid audience"
            ) from exc
        except jwt.InvalidIssuerError as exc:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Invalid issuer"
            ) from exc

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme.",
                )
            if not self.verify_jwk_token(credentials.credentials):
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
            return credentials
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail="No credentials")


def get_user_claims(
    credentials: HTTPAuthorizationCredentials = Depends(JWTBearer()),
) -> dict:
    """Get the user claims from the JWT token."""
    return jwt.decode(credentials.credentials, options={"verify_signature": False})
