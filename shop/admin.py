from django.contrib import admin

from .models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("user__username", "user__email")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet", "transaction_type", "amount", "description", "created_at")
    list_filter = ("transaction_type",)
    ordering = ("-created_at", "-id")
    search_fields = ("wallet__user__username", "wallet__user__email", "description")
