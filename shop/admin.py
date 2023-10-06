from django.contrib import admin

from .models import *

admin.site.register(Format)
admin.site.register(Country)
admin.site.register(Balance)
admin.site.register(Product)
admin.site.register(ProductLink)
admin.site.register(Purchase)
admin.site.register(PurchaseLink)
