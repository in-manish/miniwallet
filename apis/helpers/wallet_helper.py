from .transaction_helper import TransactionHelper
from rest_framework.exceptions import ValidationError


class WalletHelper:
    def __init__(self, owned_by):
        self.owned_by = owned_by
        self.wallet = self._get_wallet()

    def _get_wallet(self):
        return self.owned_by.customer_wallet

    def deposit(self, amount, reference_id):
        obj = TransactionHelper(self.owned_by, amount, reference_id)
        transaction = obj.create_transaction(is_deposit=True)
        self.wallet.amount += amount
        self.wallet.save()
        return self.wallet, transaction

    def withdraws(self, amount, reference_id):
        if self.wallet.amount - amount < 0:
            raise ValidationError(f"Insufficient balance in your to withdraw!")

        obj = TransactionHelper(self.owned_by, amount, reference_id)
        transaction = obj.create_transaction(is_deposit=False)
        self.wallet.amount -= amount
        self.wallet.save()
        return self.wallet, transaction
