from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError
import hashlib
from hashlib import md5

from .forms import PaymentForm
from .service import get_payment_link


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


class QiwiPaymentSystem(View):
    def get(self, request):
        merchant_id = '35421'
        order_amount = '100'
        currency = 'RUB'
        order_id = '1'
        secret_word = 'wrRI*,Y}nau9Z4O'
        sign = md5(f'{merchant_id}:{order_amount}:{secret_word}:{currency}:{order_id}'.encode('utf-8')).hexdigest()
        context = {
            'm': merchant_id,
            'oa': order_amount,
            'o': order_id,
            's': sign,
            'currency': currency
        }
        return render(request, 'payment/qiwi_payment_system.html', context)

    def post(self, request):
        payment_system_id = 35
        email = 'normikp@gmail.com'
        ip = '192.168.1.8'
        payment_form = PaymentForm(request.POST)
        payment = payment_form.save(commit=False)
        amount = float(payment.amount)
        link = get_payment_link(payment_system_id, email, ip, amount)
        return redirect(link)
