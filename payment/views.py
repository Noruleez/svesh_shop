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
        form = PaymentForm()
        return render(request, 'payment/freekassa_payment_system.html', context={'form': form})
    def post(self, request):
        bound_form = PaymentForm(request.POST)
        if bound_form.is_valid():
            new_form = bound_form.save(commit=False)
            FreeKassaPaymentStatus.objects.create(user=request.user, amount=new_form.amount, status='WaitPayment')
        return redirect('/payment/freekassa-payment-system-status/')
        # return render(request, 'shop/product_detail.html', context={'form': bound_purchase_form})

class FreeKassaPaymentSystemStatus(View):
    def get(self, request):
        # user_payment = FreeKassaPaymentStatus.objects.get(user=request.user, status = 'WaitPayment')
        # order_amount = f'{user_payment.amount}'
        order_amount = '111'
        merchant_id = '35421'
        currency = 'RUB'
        # order_id = f'{request.user.id}'
        order_id = '11'
        secret_word = 'wrRI*,Y}nau9Z4O'
        sign = md5(f'{merchant_id}:{order_amount}:{secret_word}:{currency}:{order_id}'.encode('utf-8')).hexdigest()
        context = {
            'm': merchant_id,
            'oa': order_amount,
            'o': order_id,
            's': sign,
            'currency': currency
        }
        return render(request, 'payment/freekassa_payment_system_status.html', context)
