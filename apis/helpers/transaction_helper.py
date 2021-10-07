
from apis.models import Wallet, Transaction
from rest_framework.exceptions import ValidationError
from apis.serializers import TransactionSerializer


class TransactionHelper:
    def __init__(self, owned_by, amount, reference_id):
        self.owned_by = owned_by
        self.wallet = get_user_wallet(owned_by)
        self.amount = amount
        self.reference_id = reference_id

    def _get_data(self):
        return {
            'amount': self.amount,
            'reference_id': self.reference_id
        }

    def create_transaction(self, is_deposit):
        if self.wallet.status != Wallet.enabled:
            raise ValidationError(f"your wallet is not active")
        data = self._get_data()
        data['status'] = Transaction.success
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(wallet=self.wallet, is_deposit=is_deposit)
        return serializer.instance


def get_user_wallet(owned_by):
    try:
        wallet = Wallet.objects.get(owned_by=owned_by)
    except Wallet.DoesNotExist:
        raise ValidationError("wallet have initialized for this user")
    return wallet
