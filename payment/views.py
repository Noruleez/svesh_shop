from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
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
            if len(FreeKassaPaymentStatus.objects.filter(user=request.user)) == 1:
                already_exists_payment = FreeKassaPaymentStatus.objects.get(user=request.user)
                already_exists_payment.delete()
                FreeKassaPaymentStatus.objects.create(user=request.user, amount=new_form.amount, status='WaitPayment')
            else:
                FreeKassaPaymentStatus.objects.create(user=request.user, amount=new_form.amount, status='WaitPayment')
        return redirect('/payment/freekassa-payment-system-status/')


class FreeKassaPaymentSystemStatus(View):
    def get(self, request):
        if request.user.is_anonymous or len(FreeKassaPaymentStatus.objects.filter(user=request.user, status = 'WaitPayment')) != 1:
            return redirect('/')
        user_payment = FreeKassaPaymentStatus.objects.get(user=request.user, status = 'WaitPayment')
        order_amount = f'{user_payment.amount}'
        merchant_id = '35421'
        currency = 'RUB'
        order_id = f'{user_payment.user}'
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
