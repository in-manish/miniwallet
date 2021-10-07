from rest_framework.serializers import ModelSerializer
from apis.models import Wallet


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        exclude = ('created_at',)

    def to_representation(self, instance):
        data = super(WalletSerializer, self).to_representation(instance)
        data['owned_by'] = instance.owned_by.customer_xid
        return data
