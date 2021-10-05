from rest_framework.authentication import TokenAuthentication
from apis.models import Wallet
from apis.serializers import WalletSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound
from accounts.models import User


class RetrieveEnableDisableWalletAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = WalletSerializer

    def get_object(self):
        user = self.request.user
        try:
            wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            raise NotFound(f"wallet have not created")
        return wallet

    def is_disabled(self):
        data = self.request.data
        is_disabled = data.get('is_disabled')
        if not isinstance(is_disabled, bool):
            raise ValidationError(f"Pleas add valid value for 'is_disabled'")
        return is_disabled

    def get_response(self, serializer):
        data = serializer.data
        return Response(data)

    def get(self, request, *args, **kwargs):
        wallet = self.get_object()
        serializer = self.serializer_class(instance=wallet)
        return self.get_response(serializer)

    def patch(self, request, *args, **kwargs):
        wallet = self.get_object()
        disable = self.is_disabled()
        if disable:
            wallet.status = Wallet.DISABLED
        else:
            wallet.status = wallet.ACTIVE
        serializer = self.serializer_class(instance=wallet)
        return self.get_response(serializer)

    def post(self, request, *args, **kwargs):
        wallet = self.get_object()
        wallet.status = Wallet.ACTIVE
        wallet.save()
        serializer = self.serializer_class(wallet)
        return self.get_response(serializer)


