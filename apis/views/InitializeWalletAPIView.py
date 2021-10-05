from django.db.utils import IntegrityError

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

from miniwallet.permissions import IsAdminOrStaff

from accounts.models import User
from apis.models import Wallet
from apis.serializers import WalletSerializer


class InitializeWalletAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrStaff,)
    serializer_class = WalletSerializer

    def get_customer(self):
        data = self.request.data
        customer_id = data.get('customer_xid')
        try:
            customer = User.objects.get(customer_xid=customer_id)
        except User.DoesNotExist:
            raise NotFound(f"customer:'{customer_id}' not found!")
        return customer

    def initiate_wallet(self, customer):
        try:
            wallet = Wallet.objects.create(user=customer, created_by=self.request.user)
        except IntegrityError:
            raise ValidationError(f"wallet already initialized for customer")
        return wallet

    def post(self, request, *args, **kwargs):
        customer = self.get_customer()
        wallet = self.initiate_wallet(customer)
        response_data = WalletSerializer(wallet).data
        return Response(data=response_data, status=status.HTTP_201_CREATED)





