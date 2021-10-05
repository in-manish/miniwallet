from rest_framework.serializers import ModelSerializer
from apis.models import Wallet


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
