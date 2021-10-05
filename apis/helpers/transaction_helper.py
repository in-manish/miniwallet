
from apis.models import Wallet
from rest_framework.exceptions import ValidationError
from apis.serializers import TransactionSerializer


class TransactionHelper:
    def __init__(self, user, amount, reference_id):
        self.user = user
        self.wallet = get_user_wallet(user)
        self.amount = amount
        self.reference_id = reference_id

    def _get_data(self):
        return {
            'wallet': self.wallet,
            'amount': self.amount,
            'reference_id': self.reference_id
        }

    def create_transaction(self):
        data = self._get_data()
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.instance


def get_user_wallet(user):
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoestNotExist:
        raise ValidationError("wallet have initialized for this user")
    return wallet