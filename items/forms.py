from django import forms

from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["description", "location", "date", "photo"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        help_texts = {
            "description": "Describe the item in your own words — colour, brand, anything distinctive.",
        }
