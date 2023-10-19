from django.db import models
from django.contrib.auth.models import User


class FreeKassaPaymentStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time_create = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(db_index=True)
    status = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount} | Статус оплаты - {self.status}'


class AaioPaymentStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time_create = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(db_index=True)
    status = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount} | Статус оплаты - {self.status}'
