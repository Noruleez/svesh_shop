from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError

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
        form = PaymentForm()
        return render(request, 'payment/qiwi_payment_system.html', context={'form': form})

    def post(self, request):
        payment_system_id = 35
        email = 'normikp@gmail.com'
        ip = '192.168.1.8'
        payment_form = PaymentForm(request.POST)
        payment = payment_form.save(commit=False)
        amount = payment.amount()
        link = get_payment_link(payment_system_id, email, ip, amount)
        return redirect(link)