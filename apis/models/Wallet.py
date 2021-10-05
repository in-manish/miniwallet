from django.db import models
from accounts.models import User


class Wallet(models.Model):
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'

    ACCOUNT_STATUS = (
        (ACTIVE, 'Active'),
        (DISABLED, 'Disabled'),
    )
    user = models.OneToOneField(User, related_name='user_wallet', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_wallets', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, db_index=True, default=ACTIVE, choices=ACCOUNT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
