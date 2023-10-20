from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView
from .models import Product, Format, Country, Purchase, PurchaseLink, Balance
from .forms import PurchaseForm
from .services import PurchaseLogic


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


class ProductDetail(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = PurchaseForm()
        return render(request, 'shop/product_detail.html', context={'product': product, 'form': form})

    def post(self, request, slug):
        form = PurchaseForm(request.POST)
        current_product = Product.objects.get(slug=slug)
        if form.is_valid():
            purchase_amount = form.cleaned_data['amount']
            purchase_user = request.user
            user_balance = Balance.objects.get(user=purchase_user).amount
            current_product_amount = current_product.amount
            current_product_price = current_product.price
            purchase_object = PurchaseLogic()
            data_error = purchase_object.check_error_in_form_data(current_product_amount, current_product_price,
                                                                  purchase_amount, user_balance)
            if data_error:
                return render(request, 'shop/product_detail.html', context={'product': current_product,
                                                                            'error': data_error,
                                                                            'form': form})
            new_purchase = purchase_object.create_new_purchase(current_product, current_product_amount, purchase_user,
                                                               purchase_amount, slug, user_balance)
            return redirect(new_purchase)
        return render(request, 'shop/product_detail.html', context={'product': current_product, 'form': form})


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
