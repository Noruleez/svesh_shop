from django.urls import path, re_path
from .views import *


urlpatterns = [

    re_path(r'^notify\w*', Notify.as_view(), name='notify_url'),
    re_path(r'^success\w*', Success.as_view(), name='success_url'),
    re_path(r'^fail\w*', Fail.as_view(), name='fail_url'),
    path('choose-payment-system/', ChoosePaymentSystem.as_view(), name = 'choose_payment_system_url'),
    path('freekassa-payment-system/', FreeKassaPaymentSystem.as_view(), name = 'freekassa_payment_system_url'),
    path('freekassa-payment-system-status/', FreeKassaPaymentSystemStatus.as_view(), name = 'freekassa_payment_system_status_url')
]
