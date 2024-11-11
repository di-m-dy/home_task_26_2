import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_product(name: str):
    return stripe.Product.create(name=name)


def create_price(product_id: str, amount: int):
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": product_id},
    )


def create_checkout_session(price_id: str):
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
