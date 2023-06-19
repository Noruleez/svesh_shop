from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError
from .forms import *
import hashlib
from hashlib import md5


class Notify(View):
    def get(self, request):
        return render(request, 'payment/notify.html')


class Success(View):
    def get(self, request):
        return render(request, 'payment/success.html')


class Fail(View):
    def get(self, request):
        return render(request, 'payment/fail.html')


class ChoosePaymentSystem(View):
    def get(self, request):
        return render(request, 'payment/choose_payment_system.html')


class FreeKassaPaymentSystem(View):
    def get(self, request):
        return render(request, 'payment/freekassa_payment_system_status.html')
    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.status = 'WaitPayment'
            new_form.save()


class FreeKassaPaymentSystemStatus(View):
    # def get(self, request):
    #     user_payment = FreeKassaPaymentStatus.objects.get(user=request.user, status = 'WaitPayment')
    #     order_amount = f'{user_payment.amount}'
    #     merchant_id = '35421'
    #     currency = 'RUB'
    #     order_id = f'{request.user}'
    #     secret_word = 'wrRI*,Y}nau9Z4O'
    #     sign = md5(f'{merchant_id}:{order_amount}:{secret_word}:{currency}:{order_id}'.encode('utf-8')).hexdigest()
    #     context = {
    #         'm': merchant_id,
    #         'oa': order_amount,
    #         'o': order_id,
    #         's': sign,
    #         'currency': currency
    #     }
    #     return render(request, 'payment/freekassa_payment_system_status.html', context)
    def get(self, request):
        return render(request, 'payment/freekassa_payment_system_status.html')