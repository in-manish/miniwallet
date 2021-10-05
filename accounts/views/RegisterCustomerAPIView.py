from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView

from accounts.models import User
from accounts.serializers import RegisterCustomerSerializer


class RegisterCustomerAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterCustomerSerializer
