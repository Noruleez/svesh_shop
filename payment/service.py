from freekassa_ru import Freekassa


SHOP_ID = '35421'
API_KEY = '7678346759fbd15b739deb43db93e027'
fk = Freekassa(shop_id=SHOP_ID, api_key=API_KEY)

payment_system_id = 35
email = 'normikp@gmail.com'
ip = '192.168.1.8'
amount = 300
list = fk.create_order(payment_system_id, email, ip, amount)


def get_payment_link(payment_system_id, email, ip, amount):
    payment_list = fk.create_order(payment_system_id, email, ip, amount)
    payment_link = payment_list['location']
    return payment_link
