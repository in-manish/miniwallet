from django.db import models
from .Wallet import Wallet


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='wallet_transactions', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
