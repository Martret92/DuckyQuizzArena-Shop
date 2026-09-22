from django import forms
from duckies.models import Item


class ShopFilterForm(forms.Form):
    item_type = forms.ChoiceField(
        required=False,
        choices=[("", "Todos los tipos"), *Item.ItemType.choices],
        label="Tipo",
    )
    rarity = forms.ChoiceField(
        required=False,
        choices=[("", "Todas las rarezas"), *Item.Rarity.choices],
        label="Rareza",
    )
    affordable = forms.BooleanField(
        required=False,
        label="Solo productos que puedo comprar",
    )
