from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView
from .models import Product, Format, Country, Purchase, PurchaseLink, ProductLink, Balance
from .forms import PurchaseForm


class RobotsTxtView(TemplateView):
    template_name = 'shop/robots.txt'
    content_type = 'text/plain'


class SitemapXmlView(TemplateView):
    template_name = 'shop/sitemap.xml'
    content_type = 'application/xml'


class AboutOurProject(TemplateView):
    template_name = 'shop/about_our_project.html'


class Rules(TemplateView):
    template_name = 'shop/rules.html'


class Faq(TemplateView):
    template_name = 'shop/faq.html'


class TdataInfo(TemplateView):
    template_name = 'shop/tdata_info.html'


class PhoneInfo(TemplateView):
    template_name = 'shop/phone_info.html'


class BalanceDetail(View):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'shop/balance.html')
        balance = Balance.objects.get(user=request.user)
        return render(request, 'shop/balance.html', context={'balance': balance})


class FormatsList(View):
    def get(self, request):
        formats = Format.objects.all().order_by('-title')
        return render(request, 'shop/formats_list.html', context={'formats': formats})


class FormatProductsList(View):
    def get(self, request, slug):
        format = Format.objects.get(slug=slug)
        products = Product.objects.filter(format__id=format.id).order_by('-amount')
        return render(request, 'shop/format_products_list.html', context={'products': products, 'format': format})


class CountriesList(View):
    def get(self, request):
        countries = Country.objects.all()
        return render(request, 'shop/countries_list.html', context={'countries': countries})


class CountryProductsList(View):
    def get(self, request, slug):
        country = Country.objects.get(slug=slug)
        products = Product.objects.filter(country__id=country.id).order_by('-amount')
        return render(request, 'shop/country_products_list.html', context={'products': products, 'country': country})


class ProductsList(View):
    def get(self, request):
        products = Product.objects.filter().order_by('-amount')
        return render(request, 'shop/index.html', context={'products': products})


def check_error_in_form_data(current_product_amount, purchase_amount, user_balance):
    if current_product_amount < purchase_amount:
        error = f'Аккаунтов осталось {current_product_amount} шт., вы запросили {purchase_amount}'
    elif user_balance < purchase_amount * current_product_amount:
        error = f'Вам не хватает {purchase_amount * current_product_amount - user_balance} руб., пополните баланс'
    else:
        return False
    return error


def move_amount_in_purchase(current_product_amount, purchase_amount, current_product):
    new_amount = current_product_amount - purchase_amount
    current_product.update(amount=new_amount)


def move_links_in_purchase(current_product, purchase_amount, new_purchase):
    product_links_objects = ProductLink.objects.filter(product=current_product)
    for i in range(purchase_amount):
        product_link = product_links_objects[0].link
        ProductLink.objects.get(link=product_link).delete()
        PurchaseLink.objects.create(purchase=new_purchase, link=product_link, slug=product_link)


def new_user_balance(user_balance, new_purchase, current_product, purchase_user):
    new_balance = user_balance - current_product.price * new_purchase.amount
    Balance.objects.filter(user=purchase_user).update(amount=new_balance)


class ProductDetail(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = PurchaseForm()
        return render(request, 'shop/product_detail.html', context={'product': product, 'form': form})

    def post(self, request, slug):
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase_amount = form.cleaned_data['amount']
            current_product = Product.objects.get(slug=slug)
            purchase_user = request.user

            user_balance = Balance.objects.get(user=purchase_user).amount
            current_product_amount = current_product.amount

            data_error = check_error_in_form_data(current_product_amount, purchase_amount, user_balance)
            if data_error:
                return render(request, 'shop/product_detail.html', context={'product': current_product,
                                                                            'error': data_error,
                                                                            'form': form})

            new_purchase = Purchase.objects.create(user=purchase_user, product=current_product, amount=purchase_amount)

            move_amount_in_purchase(current_product_amount, purchase_amount, current_product)

            move_links_in_purchase(current_product, purchase_amount, new_purchase)

            new_user_balance(user_balance, new_purchase, current_product, purchase_user)

            return redirect(new_purchase)

        return render(request, 'shop/product_detail.html', context={'form': form})


class PurchasesList(View):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'shop/purchases_list.html')
        purchases = Purchase.objects.filter(user=request.user).order_by('-date_time_create')
        return render(request, 'shop/purchases_list.html', context={'purchases': purchases})


class PurchaseLinksList(View):
    def get(self, request, slug):
        purchase = Purchase.objects.get(slug=slug)
        if purchase.user != request.user or request.user.is_anonymous:
            return redirect('/purchases/')
        links = PurchaseLink.objects.filter(purchase__id=purchase.id)
        return render(request, 'shop/purchase_links_list.html', context={'links': links})
