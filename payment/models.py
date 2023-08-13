from django.db import models
from django.contrib.auth.models import User


class FreeKassaPaymentStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time_create = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, db_index=True)
    status = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return f'Статус оплаты пользователя {self.user.username}: {self.status}'


class AaioPaymentStatus(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)
    date_time_create = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, db_index=True)
    status = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return f'Статус оплаты пользователя {self.user.username}: {self.status}'
