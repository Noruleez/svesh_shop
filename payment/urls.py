from django.urls import path, re_path
from .views import *


urlpatterns = [

    path('choose-payment-system/', ChoosePaymentSystem.as_view(), name='choose_payment_system_url'),


    re_path(r'^freekassa-notify\w*', FreeKassaNotify.as_view(), name='freekassa_notify_url'),
    re_path(r'^freekassa-success\w*', FreeKassaSuccess.as_view(), name='freekassa_success_url'),
    re_path(r'^freekassa-fail\w*', FreeKassaFail.as_view(), name='freekassa_fail_url'),
    path('freekassa-payment-system/', FreeKassaPaymentSystem.as_view(), name='freekassa_payment_system_url'),
    path('freekassa-payment-system-status/', FreeKassaPaymentSystemStatus.as_view(),
         name='freekassa_payment_system_status_url'),


    re_path(r'^aaio-notify\w*', AaioNotify.as_view(), name='aaio_notify_url'),
    re_path(r'^aaio-success\w*', AaioSuccess.as_view(), name='aaio_success_url'),
    re_path(r'^aaio-fail\w*', AaioFail.as_view(), name='aaio_fail_url'),
    path('aaio-payment-system/', AaioPaymentSystem.as_view(), name='aaio_payment_system_url'),
    path('aaio-payment-system-status/', AaioPaymentSystemStatus.as_view(),
         name='aaio_payment_system_status_url')

]
