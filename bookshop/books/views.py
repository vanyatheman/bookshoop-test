from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse

from .models import Book, Order
from bookshop.settings import BOOKS_PER_PAGE, DESCRIPTION_SYMBOLS

import json


def paginator(request, books):
    paginator = Paginator(books, BOOKS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


class BooksListView(ListView):
    model = Book
    template_name = 'books/index.html'
    paginate_by = BOOKS_PER_PAGE


class BooksDetailView(DetailView):
    model = Book
    template_name = 'books/detail.html'


class SearchResultsListView(ListView):
    model = Book
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(publish_date__icontains=query)  # | Q(isbn__icontains=query)
        )

class BookCheckoutView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/checkout.html'
    login_url     = 'login'


def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    product = Book.objects.get(id=body['productId'])
    Order.objects.create(
        product=product
    )
    return JsonResponse('Payment completed!', safe=False)