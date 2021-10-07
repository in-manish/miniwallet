from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError as django_ValidationError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from accounts.helper import get_token
from accounts.models import User

from apis.utils import get_fail_msg, get_success_data
from apis.helpers.wallet_helper import WalletHelper
from apis.models import Wallet, Transaction
from apis.serializers import WalletSerializer, TransactionSerializer


__all__ = (
    'InitializeWalletAPIView',
    'RetrieveEnableDisableWalletAPIView',
    'WithdrawFromWalletAPIView',
    'DepositToWalletAPIView',
)


class InitializeWalletAPIView(APIView):
    """
        Initialize Customer wallet
    """
    serializer_class = WalletSerializer

    def get_customer(self):
        data = self.request.data
        customer_id = data.get('customer_xid')
        if customer_id is None:
            error_msg = {'customer_xid': ["Missing data for required field."]}
            raise ValidationError(get_fail_msg(error_msg))
        try:
            customer = User.objects.get(customer_xid=customer_id)
        except User.DoesNotExist:
            error_msg = get_fail_msg(f"Customer Not found")
            raise NotFound(error_msg)
        except django_ValidationError:
            error_msg = get_fail_msg(f"Invalid customer id")
            raise ValidationError(error_msg)
        return customer

    def initiate_wallet(self, customer):
        try:
            wallet = Wallet.objects.create(owned_by=customer)
        except IntegrityError:
            error_msg = get_fail_msg(f"Wallet Already Initialized")
            raise ValidationError(error_msg)
        return wallet

    def post(self, request, *args, **kwargs):
        customer = self.get_customer()
        self.initiate_wallet(customer)
        token_key = get_token(customer)
        response_data = get_success_data({'token': token_key})
        return Response(data=response_data, status=status.HTTP_201_CREATED)


class RetrieveEnableDisableWalletAPIView(APIView):
    """
        View, Enable, Disable wallet
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = WalletSerializer

    def get_object(self):
        customer = self.request.user
        try:
            wallet = Wallet.objects.get(owned_by=customer)
        except Wallet.DoesNotExist:
            msg = f"wallet have not created"
            raise NotFound(get_fail_msg(msg))
        return wallet

    def is_disabled(self):
        data = self.request.data
        is_disabled = data.get('is_disabled')
        if is_disabled not in ('true', 'false'):
            msg = f"Pleas add valid value for 'is_disabled'"
            raise ValidationError(get_fail_msg(msg))
        is_disabled = True if is_disabled == 'true' else False
        return is_disabled

    def get(self, request, *args, **kwargs):
        """View Wallet"""
        wallet = self.get_object()
        if wallet.status == Wallet.disabled:
            raise ValidationError(get_fail_msg("Disabled"))
        serializer = self.serializer_class(instance=wallet)
        data = serializer.data
        data['enabled_at'] = data.pop('modified_at')
        data['balance'] = data.pop('amount')
        response_data = get_success_data(data)
        return Response(response_data)

    def patch(self, request, *args, **kwargs):
        """ Disable Wallet """
        wallet = self.get_object()
        disable = self.is_disabled()
        if disable and wallet.status == Wallet.disabled:
            raise ValidationError(get_fail_msg("Already Disabled"))
        wallet.status = Wallet.disabled
        wallet.save()
        serializer = self.serializer_class(instance=wallet)
        data = serializer.data
        response_data = get_success_data(data)
        return Response(response_data)

    def post(self, request, *args, **kwargs):
        """ Enable Wallet """
        wallet = self.get_object()
        if wallet.status == Wallet.enabled:
            raise ValidationError(get_fail_msg("Already enabled"))
        wallet.status = Wallet.enabled
        wallet.save()
        serializer = self.serializer_class(wallet)
        data = serializer.data
        data['enabled_at'] = data.pop('modified_at')
        data['balance'] = data.pop('amount')
        response_data = get_success_data(data)
        return Response(response_data)


class WithdrawFromWalletAPIView(APIView):
    """ Withdraw Amount from wallet """
    authentication_classes = (TokenAuthentication,)
    serializer_class = WalletSerializer

    def validate_data(self):
        data = self.request.data
        amount = data.get('amount')
        errors = []
        if not isinstance(amount, str) or not amount.isdigit() or int(amount) < 0:
            errors.append('Please Add valid amount')

        reference_id = data.get('reference_id')
        if Transaction.objects.filter(reference_id=reference_id).exists():
            errors.append("'reference_id' should be unique")

        if errors:
            raise ValidationError(get_fail_msg(errors))

    def get_response(self, transaction_serializer):
        response_data = {'deposit': transaction_serializer.data}
        response_data = get_success_data(data=response_data)
        return Response(data=response_data)

    def post(self, request, *args, **kwargs):
        self.validate_data()
        data = self.request.data
        amount = int(data.get('amount'))
        reference_id = data.get('reference_id')
        owned_by = self.request.user
        obj = WalletHelper(owned_by=owned_by)
        wallet_instance, transaction_instance = obj.withdraws(amount, reference_id)
        transaction_serializer = TransactionSerializer(transaction_instance)
        return self.get_response(transaction_serializer)


class DepositToWalletAPIView(APIView):
    """ Deposit amount to wallet """
    authentication_classes = (TokenAuthentication,)
    serializer_class = WalletSerializer

    def validate_data(self):
        data = self.request.data
        amount = data.get('amount')
        errors = []
        if not isinstance(amount, str) or not amount.isdigit() or int(amount) < 0:
            errors.append('Please Add valid amount')

        reference_id = data.get('reference_id')
        if Transaction.objects.filter(reference_id=reference_id).exists():
            errors.append("'reference_id' should be unique")

        if errors:
            raise ValidationError(get_fail_msg(errors))

    def get_response(self, transaction_serializer):
        response_data = {'deposit': transaction_serializer.data}
        response_data = get_success_data(data=response_data)
        return Response(data=response_data)

    def post(self, request, *args, **kwargs):
        self.validate_data()
        data = self.request.data
        amount = int(data.get('amount'))
        reference_id = data.get('reference_id')
        customer = self.request.user
        obj = WalletHelper(owned_by=customer)
        wallet_instance, transaction_instance = obj.deposit(amount, reference_id)
        transaction_serializer = TransactionSerializer(transaction_instance)
        return self.get_response(transaction_serializer)
