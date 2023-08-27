import string
import secrets
from datetime import date
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ErrorDetail


def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def validate_user_age(date_of_birth):
    min_age = 13
    age = (date.today() - date_of_birth).days // 365
    if age < min_age:
        raise ValidationError({"date_of_birth": ErrorDetail(f"You must be at least {min_age} years old.", code="minimum_age")})