from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from .models import Cart, CartItem
from .forms import CartItemForm
from books.models import Book

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    print(">>> request.user", request.user)
    total_items = cart.total_quantity
    context = {'cart': cart, 'total_items': total_items}
    return render(request, 'cart/cart.html', context)

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, book=book)

    if request.method == 'POST':
        form = modelform_factory(CartItem, fields=['quantity'])(request.POST, instance=cart_item)
        if form.is_valid():
            cart_item.quantity = form.cleaned_data['quantity']
            cart_item.save()
            return redirect('cart:cart_view')
    else:
        form = modelform_factory(CartItem, fields=['quantity'])(instance=cart_item)

    return render(request, 'cart/add_to_cart.html', {'form': form, 'book': book})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:cart_view')
