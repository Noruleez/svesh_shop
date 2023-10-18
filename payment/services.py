import hashlib
from urllib.parse import urlencode


def exists_incomplete_payment(request, instance_model):
    if len(instance_model.objects.filter(user=request.user, status='WaitPayment')) == 1:
        return True


def delete_incomplete_payment(request, instance_model):
    incomplete_payment = instance_model.objects.get(user=request.user, status='WaitPayment')
    incomplete_payment.delete()


def create_payment(request, instance_model, amount):
    instance_model.objects.create(user=request.user, amount=amount, status='WaitPayment')


def save_data_about_payment(request, form, instance_model):
    amount = form.cleaned_data['amount']
    if exists_incomplete_payment(request, instance_model):
        delete_incomplete_payment(request, instance_model)
        create_payment(request, instance_model, amount)
    else:
        create_payment(request, instance_model, amount)


def get_freekassa_redirect_url(request, instance_model):
    user_payment = instance_model.objects.get(user=request.user, status='WaitPayment')
    order_amount = f'{user_payment.amount}'
    merchant_id = '35421'
    currency = 'RUB'
    order_id = f'{user_payment.pk}'
    secret_word = 'wrRI*,Y}nau9Z4O'
    sign = hashlib.md5(f'{merchant_id}:{order_amount}:{secret_word}:{currency}:{order_id}'.encode('utf-8')
               ).hexdigest()
    params = {
        'm': merchant_id,
        'oa': order_amount,
        'o': order_id,
        's': sign,
        'currency': currency
    }
    return f'https://pay.freekassa.ru/?{urlencode(params)}'


def get_aaio_redirect_url(request, instance_model):
    user_payment = instance_model.objects.get(user=request.user, status='WaitPayment')
    merchant_id = 'ed4b0f81-7e27-4312-a2d0-4bb9f984732b'  # ID Вашего магазина
    amount = user_payment.amount  # Сумма к оплате
    currency = 'RUB'  # Валюта заказа
    secret = 'd8122ab1c6c4cdc29e9f1cb604bafc4a'  # Секретный ключ №1
    order_id = f'{user_payment.pk}'  # Идентификатор заказа в Вашей системе
    desc = 'Order Payment'  # Описание заказа
    lang = 'ru'  # Язык формы
    sign = f':'.join([
        str(merchant_id),
        str(amount),
        str(currency),
        str(secret),
        str(order_id)
    ])
    params = {
        'merchant_id': merchant_id,
        'amount': amount,
        'currency': currency,
        'order_id': order_id,
        'sign': hashlib.sha256(sign.encode('utf-8')).hexdigest(),
        'desc': desc,
        'lang': lang
    }
    return f'https://aaio.io/merchant/pay?{urlencode(params)}'