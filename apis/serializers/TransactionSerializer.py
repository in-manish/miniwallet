from rest_framework.serializers import ModelSerializer
from apis.models import Transaction


class TransactionSerializer(ModelSerializer):

    class Meta:
        model = Transaction
        exclude = ('modified_at', 'wallet', 'is_deposit')

    def to_representation(self, instance):
        data = super(TransactionSerializer, self).to_representation(instance)
        customer_xid = instance.wallet.owned_by.customer_xid
        if instance.is_deposit:
            data['deposited_at'] = data.pop('created_at')
            data['deposited_by'] = customer_xid
        else:
            data['withdrawn_at'] = data.pop('created_at')
            data['withdrawn_by'] = customer_xid
        return data


