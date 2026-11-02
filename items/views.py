from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ItemForm
from .models import Item


def home(request):
    found_items = Item.objects.filter(kind=Item.Kind.FOUND, status=Item.Status.OPEN)
    my_items = (
        Item.objects.filter(reported_by=request.user)
        if request.user.is_authenticated
        else Item.objects.none()
    )
    return render(request, "items/home.html", {"found_items": found_items, "my_items": my_items})


@login_required
def report(request, kind):
    if kind not in Item.Kind.values:
        raise Http404
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.kind = kind
        item.reported_by = request.user
        item.save()
        messages.success(request, "Thanks — your report has been logged.")
        return redirect("items:detail", pk=item.pk)
    return render(request, "items/report.html", {"form": form, "kind": kind})


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "items/detail.html", {"item": item})


def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("items:home")
    return render(request, "registration/signup.html", {"form": form})
