import uuid
from django.db import models
from .Wallet import Wallet


class Transaction(models.Model):
    success = 'success'
    failed = 'failed'
    STATUS_CHOICES = (
        (success, success),
        (failed, failed)
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, related_name='wallet_transactions', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    is_deposit = models.BooleanField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    reference_id = models.CharField(unique=True, db_index=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
