from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError


class Notify(View):
    def get(self, request):
        return render(request, 'payment/notify.html')


class Success(View):
    def get(self, request):
        return render(request, 'payment/success.html')


class Fail(View):
    def get(self, request):
        return render(request, 'payment/fail.html')
