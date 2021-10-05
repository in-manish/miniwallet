from rest_framework.views import  APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from apis.models import Transaction
from apis.helpers.wallet_helper import WalletHelper
from apis.serializers import WalletSerializer, TransactionSerializer
from rest_framework.response import Response


class DepositToWalletAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = WalletSerializer

    def validate_data(self):
        data = self.request.data
        amount = data.get('amount')
        errors = []
        if not isinstance(amount, int) or amount < 0:
            errors.append('Please Add valid amount')

        reference_id = data.get('reference_id')
        if Transaction.objects.filter(reference_id=reference_id).exists():
            errors.append("'reference_id' should be unique")

        if errors:
            raise ValidationError(errors)

    def post(self, request, *args, **kwargs):
        self.validate_data()
        data = self.request.data
        amount = data.get('amount')
        reference_id = data.get('reference_id')
        user = self.request.user
        obj = WalletHelper(user=user)
        wallet_instance, transaction_instance = obj.deposit(amount, reference_id)
        response_data = WalletSerializer(wallet_instance).data
        response_data['transaction'] = TransactionSerializer(wallet_instance).data
        return Response(data=response_data)
