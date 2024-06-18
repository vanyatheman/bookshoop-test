from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.BooksListView.as_view(), name="index"),
    path("books/<int:pk>/", views.BooksDetailView.as_view(), name="detail"),
    path(
        "books/search/",
        views.SearchResultsListView.as_view(),
        name="search_results"
    ),
]
