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


class FindForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="What did you lose?",
        widget=forms.TextInput(attrs={"placeholder": "e.g. black Nike backpack with a keyring"}),
    )
    object_type = forms.ChoiceField(
        required=False, label="Category", choices=[("", "Any category")] + Item.Category.choices
    )
    colour = forms.ChoiceField(
        required=False, label="Colour", choices=[("", "Any colour")] + Item.Colour.choices
    )
    location = forms.CharField(
        required=False, label="Where", widget=forms.TextInput(attrs={"placeholder": "e.g. Library"})
    )
    lost_on = forms.DateField(
        required=False,
        label="Lost on or after",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
