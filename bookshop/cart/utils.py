import stripe
from django.conf import settings

from .models import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_cart_with_items(cart_id, user):
    try:
        return (
            Cart
            .objects
            .select_related('user')
            .prefetch_related('items__book')
            .get(pk=cart_id, user=user)
        )
    except Cart.DoesNotExist:
        return None


def create_line_items(cart):
    line_items = [
        {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.book.title,
                },
                'unit_amount': int(item.book.price * 100),
            },
            'quantity': item.quantity,
        }
        for item in cart.items.all()
    ]
    return line_items


def create_stripe_checkout_session(line_items, domain_url, cart):
    return stripe.checkout.Session.create(
        success_url=(
            domain_url
            + 'cart/success?session_id={CHECKOUT_SESSION_ID}'
        ),
        cancel_url=domain_url + 'cart/cancelled/',
        payment_method_types=['card'],
        mode='payment',
        line_items=line_items,
        metadata={
            'cart_id': str(cart.id)
        }
    )


def clear_cart(session):
    cart_id = session.get('metadata', {}).get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.get(pk=cart_id)
            cart.items.all().delete()
            cart.save()
        except Cart.DoesNotExist:
            pass
