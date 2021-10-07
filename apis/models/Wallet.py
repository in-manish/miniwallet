import uuid
from django.db import models
from accounts.models import User


class Wallet(models.Model):
    enabled = 'enabled'
    disabled = 'disabled'

    ACCOUNT_STATUS = (
        (enabled, 'enabled'),
        (disabled, 'disabled'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owned_by = models.OneToOneField(User, related_name='customer_wallet', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, db_index=True, default=enabled, choices=ACCOUNT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
