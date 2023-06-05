from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core.exceptions import ValidationError

from .models import Product, Format, Country, Purchase, PurchaseLink, ProductLink, Balance
from .forms import PurchaseForm
from .utils import ObjectDetailMixin


class Rules(View):
    def get(self, request):
        return render(request, 'shop/rules.html')


class TdataInfo(View):
    def get(self, request):
        return render(request, 'shop/tdata_info.html')


class BalanceDetail(View):
    def get(self, request):
        balance = Balance.objects.get(user=request.user)
        return render(request, 'shop/balance.html', context={'balance': balance})


class FormatsList(View):
    def get(self, request):
        formats = Format.objects.all()
        return render(request, 'shop/formats_list.html', context={'formats': formats})


class FormatProductsList(View):
    def get(self, request, slug):
        format = Format.objects.get(slug=slug)
        products = Product.objects.filter(format__id=format.id).order_by('delay')
        return render(request, 'shop/format_products_list.html', context={'products': products})


class CountriesList(View):
    def get(self, request):
        countries = Country.objects.all()
        return render(request, 'shop/countries_list.html', context={'countries': countries})


class CountryProductsList(View):
    def get(self, request, slug):
        country = Country.objects.get(slug=slug)
        products = Product.objects.filter(country__id=country.id).order_by('delay')
        return render(request, 'shop/country_products_list.html', context={'products': products})


class ProductsList(View):
    def get(self, request):
        products = Product.objects.all().order_by('delay')
        return render(request, 'shop/index.html', context={'products': products})


class ProductDetail(View):
    # ObjectDetailMixin
    # model = Product
    # template = 'shop/product_detail.html'
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = PurchaseForm()
        return render(request, 'shop/product_detail.html', context={'product': product, 'form': form})

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        bound_purchase_form = PurchaseForm(request.POST)
        if bound_purchase_form.is_valid():
            new_purchase = bound_purchase_form.save(commit=False)
            # Check amount purchase > 0
            if new_purchase.amount <= 0:
                error_0_amount = 'Количество аккаунтов не может быть равным нулю или отрицательным'
                return render(request, 'shop/product_detail.html', context={'product': product,
                                                                            'error_balance': error_0_amount,
                                                                            'form': bound_purchase_form})
            # Check product amount
            if product.amount < new_purchase.amount:
                error_amount = f'Аккаунтов осталось {product.amount} шт., вы запросили {new_purchase.amount}'
                return render(request, 'shop/product_detail.html', context={'product': product,
                                                                            'error_balance': error_amount,
                                                                            'form': bound_purchase_form})
            # Check balance
            user_balance = Balance.objects.get(user=request.user).amount
            if user_balance < new_purchase.amount * product.price:
                # return redirect('/')
                error_balance = f'Вам не хватает {new_purchase.amount * product.price - user_balance} руб., пополните баланс'
                return render(request, 'shop/product_detail.html', context={'product': product,
                                                                            'error_balance': error_balance,
                                                                            'form': bound_purchase_form})
            new_purchase.product = product
            new_purchase.user = request.user
            new_purchase = bound_purchase_form.save()
            # Move amount
            new_amount = product.amount - new_purchase.amount
            Product.objects.filter(slug=slug).update(amount=new_amount)
            # Move links
            product_links_objects = ProductLink.objects.filter(product=product)
            for i in range(new_purchase.amount):
                product_link = product_links_objects[0].link
                ProductLink.objects.get(link=product_link).delete()
                PurchaseLink.objects.create(purchase=new_purchase, link=product_link, slug=product_link)
            # Move balance
            user_balance = Balance.objects.get(user=request.user).amount
            new_balance = user_balance - product.price * new_purchase.amount
            Balance.objects.filter(user=request.user).update(amount=new_balance)
            return redirect(new_purchase)

        return render(request, 'shop/product_detail.html', context={'form': bound_purchase_form})


class PurchasesList(View):
    def get(self, request):
        purchases = Purchase.objects.filter(user=request.user)
        return render(request, 'shop/purchases_list.html', context={'purchases': purchases})


class PurchaseLinksList(View):
    def get(self, request, slug):
        purchase = Purchase.objects.get(slug=slug)
        links = PurchaseLink.objects.filter(purchase__id=purchase.id)
        return render(request, 'shop/purchase_links_list.html', context={'links': links})
