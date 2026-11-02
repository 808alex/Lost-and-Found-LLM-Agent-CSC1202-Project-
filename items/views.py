from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from . import agent
from .forms import FindForm, ItemForm
from .models import Item


@login_required
def home(request):
    found_items = Item.objects.filter(kind=Item.Kind.FOUND, status=Item.Status.OPEN)
    return render(request, "items/home.html", {"found_items": found_items})


@login_required
def find(request):
    return render(request, "items/find.html", {"form": FindForm()})


@login_required
def results(request):
    form = FindForm(request.GET)
    if not form.is_valid() or not any(form.cleaned_data.values()):
        return redirect("items:find")
    data = form.cleaned_data

    # What the agent understood from the person's own words.
    understood = agent.extract_attributes(data["q"])

    items = Item.objects.filter(kind=Item.Kind.FOUND, status=Item.Status.OPEN)
    # Filters narrow the list down; the agent then ranks what's left.
    if data["object_type"]:
        items = items.filter(object_type=data["object_type"])
    if data["colour"]:
        items = items.filter(colour=data["colour"])
    if data["location"]:
        items = items.filter(location__icontains=data["location"])
    if data["lost_on"]:
        items = items.filter(date__gte=data["lost_on"])
    matches = agent.find_matches(data["q"], items)

    return render(request, "items/results.html", {
        "query": data["q"],
        "understood": {
            "category": Item.Category(understood["object_type"]).label if "object_type" in understood else "",
            "colour": Item.Colour(understood["colour"]).label if "colour" in understood else "",
        },
        "results": matches,
    })


@login_required
def report(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.kind = Item.Kind.LOST
        item.reported_by = request.user
        for field, value in agent.extract_attributes(item.description).items():
            setattr(item, field, value)
        item.save()
        messages.success(request, "Thanks — your report has been logged.")
        return redirect("items:detail", pk=item.pk)
    return render(request, "items/report.html", {"form": form})


@login_required
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "items/detail.html", {"item": item})
