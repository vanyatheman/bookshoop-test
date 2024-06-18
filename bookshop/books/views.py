from django.db.models import Q
from django.views.generic import DetailView, ListView

from bookshop.settings import BOOKS_PER_PAGE
from cart.models import Cart

from .models import Book


def get_total_items(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        total_items = cart.total_quantity if cart else 0
    else:
        total_items = 0

    return total_items


class BooksListView(ListView):
    model = Book
    template_name = "books/index.html"
    paginate_by = BOOKS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_items = get_total_items(self.request)
        context["total_items"] = total_items
        return context


class BooksDetailView(DetailView):
    model = Book
    template_name = "books/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_items = get_total_items(self.request)
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
        total_items = get_total_items(self.request)
        context["total_items"] = total_items
        return context
