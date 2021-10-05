from rest_framework.serializers import ModelSerializer

from accounts.models import User


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('user_permissions', 'groups')
