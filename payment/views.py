from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from .models import FreeKassaPaymentStatus, AaioPaymentStatus
from shop.models import Balance
from .forms import FreeKassaPaymentForm, AaioPaymentForm
import hashlib
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from urllib.parse import urlencode
from decimal import *


class ChoosePaymentSystem(TemplateView):
    template_name = 'payment/choose_payment_system.html'


def exists_incomplete_payment(request, instance_model):
    if len(instance_model.objects.filter(user=request.user, status='WaitPayment')) == 1:
        return True


def delete_incomplete_payment(request, instance_model):
    incomplete_payment = instance_model.objects.get(user=request.user, status='WaitPayment')
    incomplete_payment.delete()


def create_payment(request, instance_model, amount):
    instance_model.objects.create(user=request.user, amount=amount, status='WaitPayment')


def save_data_about_payment(request, form, instance_model):
    amount = form.cleaned_data['amount']
    if exists_incomplete_payment(request, instance_model):
        delete_incomplete_payment(request, instance_model)
        create_payment(request, instance_model, amount)
    else:
        create_payment(request, instance_model, amount)


class FreeKassaPaymentSystem(View):
    def get(self, request):
        form = FreeKassaPaymentForm()
        return render(request, 'payment/freekassa_payment_system.html', context={'form': form})

    def post(self, request):
        form = FreeKassaPaymentForm(request.POST)
        if form.is_valid():
            save_data_about_payment(request, form, instance_model=FreeKassaPaymentStatus)
            return redirect('/payment/freekassa-payment-system-status/')
        return render(request, 'payment/freekassa_payment_system.html', context={'form': form})


# class FreeKassaPaymentSystem(View):
#     def get(self, request):
#         form = FreeKassaPaymentForm()
#         return render(request, 'payment/freekassa_payment_system.html', context={'form': form})
#
#     def post(self, request):
# if form.is_valid():
#     new_form = form.save(commit=False)
#     if len(FreeKassaPaymentStatus.objects.filter(user=request.user, status='WaitPayment')) == 1:
#         already_exists_payment = FreeKassaPaymentStatus.objects.get(user=request.user, status='WaitPayment')
#         already_exists_payment.delete()
#         FreeKassaPaymentStatus.objects.create(user=request.user, amount=new_form.amount, status='WaitPayment')
#     else:
#         FreeKassaPaymentStatus.objects.create(user=request.user, amount=new_form.amount, status='WaitPayment')
#     return redirect('/payment/freekassa-payment-system-status/')
# else:
#     return render(request, 'payment/freekassa_payment_system.html', context={'form': form})


class AaioPaymentSystem(View):
    def get(self, request):
        form = AaioPaymentForm()
        return render(request, 'payment/aaio_payment_system.html', context={'form': form})

    def post(self, request):
        form = AaioPaymentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            if len(AaioPaymentStatus.objects.filter(user=request.user, status='WaitPayment')) == 1:
                already_exists_payment = AaioPaymentStatus.objects.get(user=request.user, status='WaitPayment')
                already_exists_payment.delete()
                AaioPaymentStatus.objects.create(user=request.user, amount=new_form.amount, status='WaitPayment')
            else:
                AaioPaymentStatus.objects.create(user=request.user, amount=new_form.amount, status='WaitPayment')
            return redirect('/payment/aaio-payment-system-status/')
        else:
            return render(request, 'payment/aaio_payment_system.html', context={'form': form})


class FreeKassaPaymentSystemStatus(View):
    def get(self, request):
        if request.user.is_anonymous or len(
                FreeKassaPaymentStatus.objects.filter(user=request.user, status='WaitPayment')) != 1:
            return redirect('/')
        user_payment = FreeKassaPaymentStatus.objects.get(user=request.user, status='WaitPayment')

        order_amount = f'{user_payment.amount}'
        merchant_id = '35421'
        currency = 'RUB'
        order_id = f'{user_payment.pk}'
        secret_word = 'wrRI*,Y}nau9Z4O'
        sign = md5(f'{merchant_id}:{order_amount}:{secret_word}:{currency}:{order_id}'.encode('utf-8')).hexdigest()

        params = {
            'm': merchant_id,
            'oa': order_amount,
            'o': order_id,
            's': sign,
            'currency': currency
        }

        url = "https://pay.freekassa.ru/?" + urlencode(params)
        return redirect(url)


class AaioPaymentSystemStatus(View):
    def get(self, request):
        if request.user.is_anonymous or len(
                AaioPaymentStatus.objects.filter(user=request.user, status='WaitPayment')) != 1:
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


@method_decorator(csrf_exempt, name='dispatch')
class FreeKassaNotify(View):
    def get(self, request):
        return render(request, 'payment/freekassa_notify.html')

    def post(self, request):
        order_id = request.POST["MERCHANT_ORDER_ID"]
        amount = request.POST["AMOUNT"]
        payment = FreeKassaPaymentStatus.objects.get(pk=int(order_id))
        user_id = payment.user.id
        user_balance = Balance.objects.get(user=user_id)
        user_balance.amount = user_balance.amount + Decimal(amount)
        user_balance.save()
        payment.status = "SuccessPayment"
        payment.save()
        return render(request, 'payment/freekassa_notify.html')


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


class FreeKassaSuccess(View):
    def get(self, request):
        order_id = request.GET.get("MERCHANT_ORDER_ID")
        payment = FreeKassaPaymentStatus.objects.get(pk=int(order_id))
        user_id = payment.user.id
        user_email = (User.objects.get(id=user_id)).email
        amount = payment.amount
        return render(request, 'payment/aaio_success.html', context={'user_email': user_email, 'amount': amount})


class AaioSuccess(View):
    def get(self, request):
        order_id = request.GET.get("order_id")
        payment = AaioPaymentStatus.objects.get(pk=int(order_id))
        user_id = payment.user.id
        user_email = (User.objects.get(id=user_id)).email
        amount = request.GET.get("amount")
        return render(request, 'payment/aaio_success.html', context={'user_email': user_email, 'amount': amount})


class FreeKassaFail(TemplateView):
    template_name = 'payment/freekassa_fail.html'


class AaioFail(TemplateView):
    template_name = 'payment/aaio_fail.html'
