from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import FreeKassaPaymentStatus, AaioPaymentStatus
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
            payment_object = Payment()
            payment_object.save_data_about_payment(request, form, instance_model)
            return redirect(payment_object.get_freekassa_redirect_url(request, instance_model))
        return render(request, 'payment/freekassa_payment_system.html', context={'form': form})


class AaioPaymentSystem(View):
    def get(self, request):
        form = AaioPaymentForm()
        return render(request, 'payment/aaio_payment_system.html', context={'form': form})

    def post(self, request):
        form = AaioPaymentForm(request.POST)
        instance_model = AaioPaymentStatus
        if form.is_valid():
            payment_object = Payment()
            payment_object.save_data_about_payment(request, form, instance_model)
            return redirect(payment_object.get_aaio_redirect_url(request, instance_model))
        return render(request, 'payment/aaio_payment_system.html', context={'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class FreeKassaNotify(View):
    def get(self, request):
        return render(request, 'payment/freekassa_notify.html')

    def post(self, request):
        payment_object = Payment()
        payment_object.change_status_payment_to_success(request,
                                                        model=FreeKassaPaymentStatus,
                                                        name_payment_system='freekassa')
        return render(request, 'payment/freekassa_notify.html')


@method_decorator(csrf_exempt, name='dispatch')
class AaioNotify(View):
    def get(self, request):
        return render(request, 'payment/aaio_notify.html')

    def post(self, request):
        payment_object = Payment()
        payment_object.change_status_payment_to_success(request,
                                                        model=AaioPaymentStatus,
                                                        name_payment_system='aaio')
        return render(request, 'payment/aaio_notify.html')


class FreeKassaSuccess(View):
    def get(self, request):
        payment = FreeKassaPaymentStatus.objects.get(pk=int(request.GET.get("MERCHANT_ORDER_ID")))
        user_email = (User.objects.get(id=payment.user.id)).email
        return render(request, 'payment/aaio_success.html', context={'user_email': user_email,
                                                                     'amount': payment.amount})


class AaioSuccess(View):
    def get(self, request):
        payment = AaioPaymentStatus.objects.get(pk=int(request.GET.get("order_id")))
        user_email = (User.objects.get(id=payment.user.id)).email
        return render(request, 'payment/aaio_success.html', context={'user_email': user_email,
                                                                     'amount': request.GET.get("amount")})


class FreeKassaFail(TemplateView):
    template_name = 'payment/freekassa_fail.html'


class AaioFail(TemplateView):
    template_name = 'payment/aaio_fail.html'
