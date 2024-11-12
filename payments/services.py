import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_product(name: str):
    """
    Создание продукта в Stripe
    :param name: название продукта
    :return: Stripe.Product
    """
    return stripe.Product.create(name=name)


def create_price(product_id: str, product_name: str, amount: int):
    """
    Создание цены в Stripe
    :param product_id: id продукта
    :param product_name: название продукта
    :param amount: цена в копейках
    :return: Stripe.Price
    """
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": product_name},
    )


def create_checkout_session(price_id: str):
    """
    Создание сессии для оплаты в Stripe
    :param price_id: id цены
    :return: Stripe.Checkout.Session
    """
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=settings.SUCCESS_PAYMENT_URL,
        cancel_url=settings.CANCEL_PAYMENT_URL
    )
