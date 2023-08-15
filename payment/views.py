from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from .models import *
from shop.models import *
from .forms import *
import hashlib
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from urllib.parse import urlencode
from decimal import *


class ChoosePaymentSystem(View):
    def get(self, request):
        return render(request, 'payment/choose_payment_system.html')


@method_decorator(csrf_exempt, name='dispatch')
class FreeKassaNotify(View):
    def get(self, request):
        return render(request, 'payment/freekassa_notify.html')
    def post(self, request):
        form_data = request.POST
        return render(request, 'payment/freekassa_notify.html', context={'form_data': form_data})


class FreeKassaSuccess(View):
    def get(self, request):
        order_id = request.GET.get("MERCHANT_ORDER_ID")
        user_email = request.user.email
        if request.user.is_anonymous:
            return redirect('/')
        #Тестовый вариант - get, поменять на post
        if user_email == order_id and FreeKassaPaymentStatus.objects.filter(user=request.user) == 1:
            payment = FreeKassaPaymentStatus.objects.get(user=request.user)
            payment.status = 'SuccessPayment'
            payment.save()
            balance = Balance.objects.get(user=request.user)
            balance.amount = balance.amount + payment.amount
            balance.save()
        else:
            return redirect('/payment/fail')
        return render(request, 'payment/freekassa_success.html', context={'order_id': order_id})


class FreeKassaFail(View):
    def get(self, request):
        return render(request, 'payment/freekassa_fail.html')


class FreeKassaPaymentSystem(View):
    def get(self, request):
        form = FreeKassaPaymentForm()
        return render(request, 'payment/freekassa_payment_system.html', context={'form': form})
    def post(self, request):
        bound_form = FreeKassaPaymentForm(request.POST)
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
        if request.user.is_anonymous or len(FreeKassaPaymentStatus.objects.filter(user=request.user, status='WaitPayment')) != 1:
            return redirect('/')
        user_payment = FreeKassaPaymentStatus.objects.get(user=request.user, status='WaitPayment')
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


@method_decorator(csrf_exempt, name='dispatch')
class AaioNotify(View):
    def get(self, request):
        return render(request, 'payment/aaio_notify.html')
    def post(self, request):
        order_id = request.POST["order_id"]
        amount = request.POST["amount"]
        payment = AaioPaymentStatus.objects.get(pk=int(order_id))
        user_id = payment.user.id
        user_balance = Balance.objects.get(user=user_id)
        user_balance.amount = user_balance.amount + Decimal(amount)
        user_balance.save()
        payment.status = "SuccessPayment"
        payment.save()
        return render(request, 'payment/aaio_notify.html')


class AaioSuccess(View):
    pass
    def get(self, request):
        order_id = request.GET.get("order_id")
        payment = AaioPaymentStatus.objects.get(pk=int(order_id))
        user_id = payment.user.id
        user_email = (User.objects.get(id=user_id)).email
        amount = request.GET.get("amount")
        return render(request, 'payment/aaio_success.html', context={'user_email': user_email, 'amount': amount})


class AaioFail(View):
    def get(self, request):
        return render(request, 'payment/aaio_fail.html')


class AaioPaymentSystem(View):
    def get(self, request):
        form = AaioPaymentForm()
        return render(request, 'payment/aaio_payment_system.html', context={'form': form})
    def post(self, request):
        bound_form = AaioPaymentForm(request.POST)
        if bound_form.is_valid():
            new_form = bound_form.save(commit=False)

            # Check payment amount
            if new_form.amount <= 0:
                error_payment_amount = 'Сумма пополнения не может быть равной нулю или отрицательной'
                return render(request, 'payment/aaio_payment_system.html', context={'error_payment_amount': error_payment_amount,
                                                                                    'form': bound_form})

            # Check integer amount
            def isint(s):
                try:
                    int(s)
                    return int(s) == float(s)
                except ValueError:
                    return False

            if not isint(new_form.amount):
                error_payment_integer_amount = 'Введите целое число'
                return render(request, 'payment/aaio_payment_system.html', context={'error_payment_amount': error_payment_integer_amount,
                                                                                    'form': bound_form})

            if len(AaioPaymentStatus.objects.filter(user=request.user, status='WaitPayment')) == 1:
                already_exists_payment = AaioPaymentStatus.objects.get(user=request.user, status='WaitPayment')
                already_exists_payment.delete()
                AaioPaymentStatus.objects.create(user=request.user, amount=new_form.amount, status='WaitPayment')
            else:
                AaioPaymentStatus.objects.create(user=request.user, amount=new_form.amount, status='WaitPayment')
        return redirect('/payment/aaio-payment-system-status/')


class AaioPaymentSystemStatus(View):
    def get(self, request):
        if request.user.is_anonymous or len(AaioPaymentStatus.objects.filter(user=request.user, status='WaitPayment')) != 1:
            return redirect('/')
        user_payment = AaioPaymentStatus.objects.get(user=request.user, status='WaitPayment')

        merchant_id = 'ed4b0f81-7e27-4312-a2d0-4bb9f984732b'  # ID Вашего магазина
        amount = user_payment.amount  # Сумма к оплате
        currency = 'RUB'  # Валюта заказа
        secret = 'd8122ab1c6c4cdc29e9f1cb604bafc4a'  # Секретный ключ №1
        order_id = f'{user_payment.pk}'  # Идентификатор заказа в Вашей системе
        desc = 'Order Payment'  # Описание заказа
        lang = 'ru'  # Язык формы

        sign = f':'.join([
            str(merchant_id),
            str(amount),
            str(currency),
            str(secret),
            str(order_id)
        ])

        params = {
            'merchant_id': merchant_id,
            'amount': amount,
            'currency': currency,
            'order_id': order_id,
            'sign': hashlib.sha256(sign.encode('utf-8')).hexdigest(),
            'desc': desc,
            'lang': lang
        }

        url = "https://aaio.io/merchant/pay?" + urlencode(params)

        return redirect(url)
