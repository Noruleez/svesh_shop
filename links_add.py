export DJANGO_SETTINGS_MODULE=mysite.settings
import django
django.setup()


from shop.models import *


country = Country.objects.get(title='Индонезия')
delay = 7
product = Product.objects.get(country=country, delay=delay)

links = []

with open('links.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        link = line[:-1]
        ProductLink.objects.create(product=product, link=link)

