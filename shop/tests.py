from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse


from .models import Wallet


class WalletTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="wallet_user", email="wallet@example.com"
        )

    def test_user_can_have_wallet(self):
        wallet = Wallet.objects.create(user=self.user)

        self.assertEqual(Wallet.objects.get(user=self.user), wallet)

    def test_wallet_is_accessible_from_user(self):
        wallet = Wallet.objects.create(user=self.user)
        user = get_user_model().objects.get(pk=self.user.pk)

        self.assertEqual(user.wallet, wallet)

    def test_user_cannot_have_two_wallets(self):
        Wallet.objects.create(user=self.user)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Wallet.objects.create(user=self.user)

        self.assertEqual(Wallet.objects.filter(user=self.user).count(), 1)

    def test_wallet_has_no_independent_balance_fields(self):
        field_names = {field.name for field in Wallet._meta.fields}

        self.assertEqual(field_names, {"id", "user", "created_at", "updated_at"})




class CatalogViewTests(TestCase):
    def test_catalog_returns_200(self):
        response = self.client.get(reverse("shop:catalog"))

        self.assertEqual(response.status_code, 200)

    def test_catalog_displays_products(self):
        response = self.client.get(reverse("shop:catalog"))

        self.assertContains(response, "Ducky Sword")
        self.assertContains(response, "Golden Shield")
        self.assertContains(response, "Ducky Potion")

    def test_product_detail_returns_200_for_existing_product(self):
        response = self.client.get(
            reverse("shop:product_detail", args=[1])
        )

        self.assertEqual(response.status_code, 200)

    def test_product_detail_displays_correct_product(self):
        response = self.client.get(
            reverse("shop:product_detail", args=[1])
        )

        self.assertContains(response, "Ducky Sword")
        self.assertContains(response, "100 Ducky Coins")

    def test_product_detail_returns_404_for_unknown_product(self):
        response = self.client.get(
            reverse("shop:product_detail", args=[999])
        )

        self.assertEqual(response.status_code, 404)
