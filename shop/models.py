from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Format(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    description = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('format_products_list_url', kwargs={'slug': self.slug})

    def __str__(self):
        return f'Формат - {self.title}'


class Country(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    description = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('country_products_list_url', kwargs={'slug': self.slug})

    def __str__(self):
        return f'Страна - {self.title}'


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, db_index=True)

    def __str__(self):
        return f'Баланс пользователя {self.user.username}: {self.amount}'


class Product(models.Model):
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    format = models.ForeignKey('Format', on_delete=models.PROTECT)
    delay = models.IntegerField(db_index=True)
    amount = models.IntegerField(db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('product_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.country} - {self.delay}-дней'


class ProductLink(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    link = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return f'Ссылка на товар {self.product}: {self.link}'


class Purchase(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, on_delete=models.PROTECT)
    amount = models.IntegerField(db_index=True)
    date_time_create = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.date_time_create)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('purchase_links_list_url', kwargs={'slug': self.slug})

    def __str__(self):
        return f'Заказ созданный - {self.date_time_create}'


class PurchaseLink(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    link = models.CharField(max_length=150, db_index=True, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return f'Ссылка на {self.purchase}'
