import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView

from books.models import Book

from .models import Cart, CartItem
from .utils import (create_line_items, create_stripe_checkout_session,
                    get_cart_with_items)


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    print(">>> request.user", request.user)
    total_items = cart.total_quantity
    context = {"cart": cart, "total_items": total_items}
    return render(request, "cart/cart.html", context)


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not book.book_available:
        return redirect("books:detail", pk=book_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, book=book)

    if request.method == "POST":
        form = modelform_factory(CartItem, fields=["quantity"])(
            request.POST, instance=cart_item
        )
        if form.is_valid():
            cart_item.quantity = form.cleaned_data["quantity"]
            cart_item.save()
            return redirect("cart:cart_view")
    else:
        form = modelform_factory(
            CartItem, fields=["quantity"]
        )(instance=cart_item)

    return render(
        request, "cart/add_to_cart.html", {"form": form, "book": book}
    )


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem, id=item_id, cart__user=request.user
    )
    cart_item.delete()
    return redirect("cart:cart_view")


class CartCheckoutView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = "cart/checkout.html"
    login_url = "login"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related(
            'items__book'
        )


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_id = data.get('cart_id')

        cart = get_cart_with_items(cart_id, request.user)
        if not cart:
            return JsonResponse({'error': 'Cart not found'}, status=404)

        line_items = create_line_items(cart)

        domain_url = 'http://localhost:8000/'
        try:
            checkout_session = create_stripe_checkout_session(
                line_items,
                domain_url,
                cart
            )
            cart.items.all().delete()
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         return HttpResponse(status=400)

#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']

#         clear_cart(session)

#     return HttpResponse(status=200)


class SuccessView(TemplateView):
    template_name = 'cart/success.html'


class CancelledView(TemplateView):
    template_name = 'cart/cancelled.html'
