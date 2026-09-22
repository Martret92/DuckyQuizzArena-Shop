from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction

from duckies.models import Ducky, InventoryItem
from duckies.services import grant_item

from .models import Transaction, Wallet


def get_wallet(user):
    wallet, _ = Wallet.objects.get_or_create(user=user)
    return wallet


def get_balance(user):
    return user.profile.ducky_coins


def _locked_profile(user):
    """Return the user's Profile row locked for the current transaction."""
    profile = user.profile
    ProfileModel = apps.get_model(profile._meta.app_label, profile._meta.model_name)
    return ProfileModel.objects.select_for_update().get(pk=profile.pk)


@transaction.atomic
def add_coins(*, user, amount, description=""):
    if amount <= 0:
        raise ValidationError("La cantidad de monedas debe ser mayor que cero.")

    profile = _locked_profile(user)
    wallet = get_wallet(user)

    profile.ducky_coins += amount
    profile.save(update_fields=["ducky_coins"])

    movement = Transaction.objects.create(
        wallet=wallet,
        transaction_type=Transaction.TransactionType.REWARD,
        amount=amount,
        description=description,
    )
    return movement


@transaction.atomic
def spend_coins(*, user, amount, description=""):
    if amount <= 0:
        raise ValidationError("La cantidad de monedas debe ser mayor que cero.")

    profile = _locked_profile(user)
    if profile.ducky_coins < amount:
        raise ValidationError("No tienes suficientes Ducky Coins.")

    wallet = get_wallet(user)
    profile.ducky_coins -= amount
    profile.save(update_fields=["ducky_coins"])

    movement = Transaction.objects.create(
        wallet=wallet,
        transaction_type=Transaction.TransactionType.PURCHASE,
        amount=-amount,
        description=description,
    )
    return movement


@transaction.atomic
def purchase_item(*, user, shop_item):
    """Validate and execute a complete Shop purchase atomically."""
    if not shop_item.is_available:
        raise ValidationError("Este producto no está disponible.")

    if not shop_item.item.is_active:
        raise ValidationError("Este objeto no está activo.")

    try:
        ducky = user.ducky
    except Ducky.DoesNotExist as exc:
        raise ValidationError("Necesitas un Ducky para comprar objetos.") from exc

    if InventoryItem.objects.filter(ducky=ducky, item=shop_item.item).exists():
        raise ValidationError("Ya tienes este objeto.")

    profile = _locked_profile(user)
    price = shop_item.price

    if profile.ducky_coins < price:
        raise ValidationError("No tienes suficientes Ducky Coins.")

    wallet = get_wallet(user)

    profile.ducky_coins -= price
    profile.save(update_fields=["ducky_coins"])

    movement = Transaction.objects.create(
        wallet=wallet,
        transaction_type=Transaction.TransactionType.PURCHASE,
        amount=-price,
        description=f"Compra de {shop_item.item.name}",
    )

    inventory_item, created = grant_item(ducky=ducky, item=shop_item.item)
    if not created:
        raise ValidationError("Ya tienes este objeto.")

    return movement, inventory_item
