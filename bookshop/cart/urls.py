from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_view, name="cart_view"),
    path("add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),
    path('config/', views.stripe_config),
    path(
        'create-checkout-session/',
        views.create_checkout_session,
        name='checkout2'
    ),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
]
