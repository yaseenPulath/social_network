from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt

from django.conf import settings
from user.jwt_utils import get_jwt_key
from user.models import User



class JWTAuthentication(BaseAuthentication):

    def is_jwt_authenticated(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', "").split('Bearer ')[-1]
        key = get_jwt_key()
        if token:
            try:
                data = jwt.decode(jwt=token, key=key, algorithms=['RS256', ])
            except jwt.ExpiredSignatureError:
                raise exceptions.NotAuthenticated("Signature has expired")
            except jwt.InvalidSignatureError:
                raise exceptions.NotAuthenticated("Signature verification failed")
            except Exception as e:
                raise exceptions.NotAuthenticated("Invalid token")
            return (data, True)
        else:
            raise exceptions.NotAuthenticated("Authentication credentials were not provided.")

    def authenticate(self, request):
        authentication_data, is_authenticated = self.is_jwt_authenticated(request)
        user_id = authentication_data.get("id")
        if(is_authenticated):
            try:
                user = User.objects.get(id=user_id)
                return (user, True)
            except Exception as e:
                raise exceptions.NotAuthenticated("Invalid token")
        return None