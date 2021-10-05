from rest_framework.serializers import ModelSerializer

from accounts.models import User


class RegisterCustomerSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('user_permissions', 'groups')

    def create(self, validated_data):
        validated_data.pop('is_staff', None)
        validated_data.pop('is_superuser', None)
        validated_data['is_customer'] = True
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        data = super(RegisterCustomerSerializer, self).to_representation(instance)
        data.pop('password')
        return data
