from django.urls import path
from .views import *


urlpatterns = [

    path('notify/', Notify.as_view(), name='notify_url'),
    path('success/', Success.as_view(), name='success_url'),
    path('fail/', Fail.as_view(), name='fail_url'),

]
