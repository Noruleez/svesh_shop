from django.urls import path
from .views import *


urlpatterns = [

    path('', ProductsList.as_view(), name='products_list_url'),
    path('product/<str:slug>/', ProductDetail.as_view(), name='product_detail_url'),

    path('formats/', FormatsList.as_view(), name='formats_list_url'),
    path('format/<str:slug>/', FormatProductsList.as_view(), name='format_products_list_url'),

    path('countries/', CountriesList.as_view(), name='countries_list_url'),
    path('country/<str:slug>', CountryProductsList.as_view(), name='country_products_list_url'),

    path('purchases/', PurchasesList.as_view(), name='purchases_list_url'),
    path('purchase/<str:slug>', PurchaseLinksList.as_view(), name='purchase_links_list_url'),

    path('balance/', BalanceDetail.as_view(), name='balance_url'),

    path('faq/', Faq.as_view(), name='faq_url'),
    path('tdata-info/', TdataInfo.as_view(), name='tdata_info_url'),
    path('phone-info/', PhoneInfo.as_view(), name='phone_info_url'),

    path('about_our_project/', AboutOurProject.as_view(), name='about_our_project_url'),
    path('rules/', Rules.as_view(), name='rules_url'),

    path('robots.txt', RobotsTxt.as_view(), content_type="text/plain", name='robots_txt_url'),

    # path('doc-offer-agreement/', DocOfferAgreement.as_view(), name='doc_offer_agreement_url'),
    # path('doc-payment-back/', DocPaymentBack.as_view(), name='doc_payment_back_url'),
    # path('doc_privacy_policy/', DocPrivacyPolicy.as_view(), name='doc_privacy_policy_url'),

]
