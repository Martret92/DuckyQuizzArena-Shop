from django.http import Http404
from django.shortcuts import render

from .catalog.data import SHOP_CATALOG


def catalog(request):
    """Display the available shop products."""
    products = SHOP_CATALOG

    return render(
        request,
        "shop/catalog.html",
        {"products": products},
    )


def product_detail(request, product_id):
    """Display the details of a single shop product."""
    product = next(
        (
            item
            for item in SHOP_CATALOG
            if item["id"] == product_id
        ),
        None,
    )

    if product is None:
        raise Http404("Producto no encontrado.")

    return render(
        request,
        "shop/product_detail.html",
        {"product": product},
    )
