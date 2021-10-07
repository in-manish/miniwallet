
from rest_framework.authtoken.models import Token


def get_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token.key
