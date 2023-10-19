from shop.models import Product, ProductLink, PurchaseLink, Balance


class PurchaseLogic:

    def check_error_in_form_data(self, current_product_amount, current_product_price,
                                 purchase_amount, user_balance):
        if current_product_amount < purchase_amount:
            error = f'Аккаунтов осталось {current_product_amount} шт., вы запросили {purchase_amount}'
        elif user_balance < purchase_amount * current_product_price:
            error = f'Вам не хватает {purchase_amount * current_product_amount - user_balance} руб., пополните баланс'
        else:
            return False
        return error

    def move_amount_in_purchase(self, current_product_amount, purchase_amount, slug):
        new_amount = current_product_amount - purchase_amount
        Product.objects.filter(slug=slug).update(amount=new_amount)

    def move_links_in_purchase(self, current_product, purchase_amount, new_purchase):
        product_links_objects = ProductLink.objects.filter(product=current_product)
        for i in range(purchase_amount):
            product_link = product_links_objects[0].link
            ProductLink.objects.get(link=product_link).delete()
            PurchaseLink.objects.create(purchase=new_purchase, link=product_link, slug=product_link)

    def new_user_balance(self, user_balance, new_purchase, current_product, purchase_user):
        new_balance = user_balance - current_product.price * new_purchase.amount
        Balance.objects.filter(user=purchase_user).update(amount=new_balance)