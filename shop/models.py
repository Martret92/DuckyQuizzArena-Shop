from django.conf import settings
from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TransactionType(models.TextChoices):
    REWARD = "REWARD"
    PURCHASE = "PURCHASE"
    ADJUSTMENT = "ADJUSTMENT"


class Transaction(models.Model):
    """Ducky Coin history; the official balance remains on user.profile."""

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.IntegerField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(transaction_type=TransactionType.REWARD, amount__gt=0)
                    | models.Q(transaction_type=TransactionType.PURCHASE, amount__lt=0)
                    | (
                        models.Q(transaction_type=TransactionType.ADJUSTMENT)
                        & ~models.Q(amount=0)
                    )
                ),
                name="shop_transaction_valid_amount",
            ),
        ]
