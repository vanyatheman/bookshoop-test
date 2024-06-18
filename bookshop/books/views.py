import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from bookshop.settings import BOOKS_PER_PAGE, DESCRIPTION_SYMBOLS
from cart.models import Cart

from .models import Book, Order


class BooksListView(ListView):
    model = Book
    template_name = "books/index.html"
    paginate_by = BOOKS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            total_items = cart.total_quantity if cart else 0
        else:
            total_items = 0

        context["total_items"] = total_items
        return context


class BooksDetailView(DetailView):
    model = Book
    template_name = "books/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            total_items = cart.total_quantity if cart else 0
        else:
            total_items = 0

        context["total_items"] = total_items
        return context


class SearchResultsListView(ListView):
    model = Book
    template_name = "books/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Book.objects.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(publish_date__icontains=query)  # | Q(isbn__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            total_items = cart.total_quantity if cart else 0
        else:
            total_items = 0

        context["total_items"] = total_items
        return context


def paymentComplete(request):
    body = json.loads(request.body)
    print("BODY:", body)
    product = Book.objects.get(id=body["productId"])
    Order.objects.create(product=product)
    return JsonResponse("Payment completed!", safe=False)
