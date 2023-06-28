from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from .forms import *
import hashlib
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token



class Notify(View):
    def get(self, request):
        return render(request, 'payment/notify.html')

    @method_decorator(requires_csrf_token)
    def post(self, request):
        p = request.POST
        return render(request, 'payment/notify.html', context={'p': p})


class Success(View):
    def get(self, request):
        order_id = request.GET.get("MERCHANT_ORDER_ID")
        return render(request, 'payment/success.html', context={'order_id': order_id})
    # def post(self, request):
    #     p = request.POST
    #     print(p)
    #     return render(request, 'payment/success.html', context={'p': p})


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
