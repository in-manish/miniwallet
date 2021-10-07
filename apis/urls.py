from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^init$', view=views.InitializeWalletAPIView.as_view(), name='initialize wallet'),

    url(r'^wallet/withdrawals$', view=views.WithdrawFromWalletAPIView.as_view(), name='withdraw amount from wallet'),

    url(r'^wallet/deposit', view=views.DepositToWalletAPIView.as_view(), name='withdraw amount from wallet'),

    url(r'^wallet$', view=views.RetrieveEnableDisableWalletAPIView.as_view(),
        name='Retrieve wallet info, Enable wallet, Disable wallet'),
]
