from django.contrib import admin

from .models import AaioPaymentStatus, FreeKassaPaymentStatus

admin.site.register(AaioPaymentStatus)
admin.site.register(FreeKassaPaymentStatus)
