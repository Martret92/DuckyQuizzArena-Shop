from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from duckies.models import InventoryItem

from .forms import ShopFilterForm
from .models import ShopItem
from .services import get_wallet, purchase_item


@login_required
def shop_home(request):
    wallet = get_wallet(request.user)
    products = (
        ShopItem.objects
        .filter(is_available=True, item__is_active=True)
        .select_related("item")
    )

    form = ShopFilterForm(request.GET or None)
    if form.is_valid():
        item_type = form.cleaned_data.get("item_type")
        rarity = form.cleaned_data.get("rarity")
        affordable = form.cleaned_data.get("affordable")

        if item_type:
            products = products.filter(item__item_type=item_type)
        if rarity:
            products = products.filter(item__rarity=rarity)
        if affordable:
            products = products.filter(price__lte=request.user.profile.ducky_coins)

    owned_item_ids = set()
    if hasattr(request.user, "ducky"):
        owned_item_ids = set(
            InventoryItem.objects.filter(ducky=request.user.ducky)
            .values_list("item_id", flat=True)
        )

    return render(request, "shop/shop_home.html", {
        "wallet": wallet,
        "products": products,
        "filter_form": form,
        "owned_item_ids": owned_item_ids,
    })


@login_required
def product_detail(request, pk):
    product = get_object_or_404(
        ShopItem.objects.select_related("item"),
        pk=pk,
    )
    wallet = get_wallet(request.user)

    already_owned = False
    if hasattr(request.user, "ducky"):
        already_owned = InventoryItem.objects.filter(
            ducky=request.user.ducky,
            item=product.item,
        ).exists()

    return render(request, "shop/product_detail.html", {
        "product": product,
        "wallet": wallet,
        "already_owned": already_owned,
    })


@login_required
def purchase(request, pk):
    product = get_object_or_404(
        ShopItem.objects.select_related("item"),
        pk=pk,
    )

    if request.method == "POST":
        try:
            purchase_item(user=request.user, shop_item=product)
        except ValidationError as error:
            messages.error(request, error.messages[0])
        else:
            messages.success(request, f"Has comprado {product.item.name}.")
        return redirect("shop:product_detail", pk=product.pk)

    return render(request, "shop/purchase_confirm.html", {
        "product": product,
        "balance": request.user.profile.ducky_coins,
        "balance_after": request.user.profile.ducky_coins - product.price,
    })


@login_required
def transaction_history(request):
    wallet = get_wallet(request.user)
    return render(request, "shop/transaction_history.html", {
        "wallet": wallet,
        "transactions": wallet.transactions.all(),
    })
