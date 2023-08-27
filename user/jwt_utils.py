from Crypto.PublicKey import RSA
from django.conf import settings
from cryptography.hazmat.primitives import serialization
import jwt
from rest_framework import exceptions

def get_jwt_key(type="public"):
    key=""
    if type == "public":
        key=settings.JWT_PUBLIC_KEY.replace('\\n', '\n').encode()
    elif type == "private":
        key=settings.JWT_PRIVATE_KEY.replace('\\n', '\n').encode()
    return key

def generate_public_and_private_key():
    key = RSA.generate(2048)
    private_key = key.exportKey()
    public_key = key.publickey().exportKey()
    return {"private_key": private_key, "public_key": public_key}

def generate_jwt_token(payload):
    private_key = get_jwt_key(type="private")
    key = serialization.load_pem_private_key(private_key,password=None)
    token = jwt.encode(payload=payload, key=key, algorithm="RS256")
    return token

def validate_jwt_token(token=None):
    if token:
        public_key = get_jwt_key()
        key = serialization.load_pem_public_key(public_key)
        try:
            data = jwt.decode(jwt=token, key=key, algorithms=['RS256', ])
        except jwt.ExpiredSignatureError:
            raise exceptions.NotAuthenticated("Signature has expired")
        except jwt.InvalidSignatureError:
            raise exceptions.NotAuthenticated("Signature verification failed")
        except Exception as e:
            raise exceptions.NotAuthenticated("Invalid token")
        return data
    else:
        raise exceptions.NotAuthenticated("Authentication credentials were not provided.")
