from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import *
from .models import FreeKassaPaymentStatus, AaioPaymentStatus
from shop.models import Balance
from .forms import FreeKassaPaymentForm, AaioPaymentForm
from .services import Payment


class ChoosePaymentSystem(TemplateView):
    template_name = 'payment/choose_payment_system.html'


class FreeKassaPaymentSystem(View):
    def get(self, request):
        form = FreeKassaPaymentForm()
        return render(request, 'payment/freekassa_payment_system.html', context={'form': form})

    def post(self, request):
        form = FreeKassaPaymentForm(request.POST)
        instance_model = FreeKassaPaymentStatus
        if form.is_valid():
            p = Payment()
            p.save_data_about_payment(request, form, instance_model)
            return redirect(p.get_freekassa_redirect_url(request, instance_model))
        return render(request, 'payment/freekassa_payment_system.html', context={'form': form})


class AaioPaymentSystem(View):
    def get(self, request):
        form = AaioPaymentForm()
        return render(request, 'payment/aaio_payment_system.html', context={'form': form})

    def post(self, request):
        form = AaioPaymentForm(request.POST)
        instance_model = AaioPaymentStatus
        if form.is_valid():
            Payment.save_data_about_payment(request, form, instance_model)
            return redirect(Payment.get_aaio_redirect_url(request, instance_model))
        return render(request, 'payment/aaio_payment_system.html', context={'form': form})


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
