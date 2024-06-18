from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from cart.models import Cart

from .forms import CreationForm, UserUpdateForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("books:index")
    template_name = "users/signup.html"


def get_total_items(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        total_items = cart.total_quantity if cart else 0
    else:
        total_items = 0

    return total_items


@login_required
def profile_view(request):

    total_items = get_total_items(request)
    context = {"total_items": total_items}
    return render(request, "users/profile.html", context=context)


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = UserUpdateForm(instance=request.user)

    total_items = get_total_items(request)
    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "total_items": total_items}
    )
