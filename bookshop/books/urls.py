from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.BooksListView.as_view(), name="index"),
    path("books/<int:pk>/", views.BooksDetailView.as_view(), name="detail"),
    # path("books/<int:pk>/checkout/", views.BookCheckoutView.as_view(), name="checkout"),
    path("books/complete/", views.paymentComplete, name="complete"),
    path("books/search/", views.SearchResultsListView.as_view(), name="search_results"),
]
