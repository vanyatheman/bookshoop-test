import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from books.models import Book
from .forms import CartItemForm
from .models import Cart, CartItem


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
    cart, created = Cart.objects.get_or_create(user=request.user)
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
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("cart:cart_view")


class CartCheckoutView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = "cart/checkout.html"
    login_url = "login"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related(
            'items__book'
        )


@login_required
def paymentComplete(request):
    body = json.loads(request.body)
    user = request.user
    cart = Cart.objects.get(user=user)

    for item in cart.items.all():
        print(f'Paid for {item.quantity} of {item.book.title}')

    cart.items.all().delete()
    
    return JsonResponse("Payment completed!", safe=False)

