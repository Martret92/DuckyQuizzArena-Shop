from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from .models import Transaction, TransactionType, Wallet


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


class TransactionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="transaction_user")
        self.wallet = Wallet.objects.create(user=self.user)

    def create_transaction(self, transaction_type=TransactionType.REWARD, amount=10):
        return Transaction.objects.create(
            wallet=self.wallet, transaction_type=transaction_type, amount=amount
        )

    def test_transaction_belongs_to_wallet(self):
        movement = self.create_transaction()
        movement.refresh_from_db()
        self.assertEqual(movement.wallet, self.wallet)

    def test_wallet_transactions_relation(self):
        movement = self.create_transaction()
        self.assertEqual(list(self.wallet.transactions.all()), [movement])

    def test_reward_accepts_positive_amount(self):
        self.assertEqual(self.create_transaction(TransactionType.REWARD, 10).amount, 10)

    def test_purchase_accepts_negative_amount(self):
        self.assertEqual(self.create_transaction(TransactionType.PURCHASE, -10).amount, -10)

    def test_adjustment_accepts_positive_amount(self):
        self.assertEqual(self.create_transaction(TransactionType.ADJUSTMENT, 10).amount, 10)

    def test_adjustment_accepts_negative_amount(self):
        self.assertEqual(self.create_transaction(TransactionType.ADJUSTMENT, -10).amount, -10)

    def test_zero_amount_is_rejected_for_every_type(self):
        for transaction_type in TransactionType:
            with self.subTest(transaction_type=transaction_type):
                with self.assertRaises(IntegrityError):
                    with transaction.atomic():
                        self.create_transaction(transaction_type, 0)

    def test_negative_reward_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_transaction(TransactionType.REWARD, -10)

    def test_positive_purchase_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_transaction(TransactionType.PURCHASE, 10)

    def test_unknown_type_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_transaction("UNKNOWN", 10)

    def test_constraint_applies_to_queryset_updates(self):
        movement = self.create_transaction()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Transaction.objects.filter(pk=movement.pk).update(amount=-10)
        movement.refresh_from_db()
        self.assertEqual(movement.amount, 10)

    def test_deleting_wallet_cascades_to_transactions(self):
        movement = self.create_transaction()
        self.wallet.delete()
        self.assertFalse(Transaction.objects.filter(pk=movement.pk).exists())

    def test_history_is_ordered_by_descending_date(self):
        newest = self.create_transaction()
        oldest = self.create_transaction()
        middle = self.create_transaction()
        now = timezone.now()
        for movement, days in [(newest, 0), (oldest, 2), (middle, 1)]:
            Transaction.objects.filter(pk=movement.pk).update(
                created_at=now - timedelta(days=days)
            )
        self.assertEqual(list(self.wallet.transactions.all()), [newest, middle, oldest])
        self.assertEqual(self.wallet.transactions.first(), newest)

    def test_history_breaks_date_ties_by_descending_id(self):
        first = self.create_transaction()
        second = self.create_transaction()
        self.wallet.transactions.update(created_at=timezone.now())
        self.assertEqual(list(self.wallet.transactions.all()), [second, first])

    def test_transaction_has_exactly_the_requested_fields(self):
        self.assertEqual(
            {field.name for field in Transaction._meta.fields},
            {"id", "wallet", "transaction_type", "amount", "description", "created_at"},
        )

    def test_transaction_has_no_independent_balance_fields(self):
        field_names = {field.name for field in Transaction._meta.fields}
        self.assertFalse(
            field_names & {"balance", "balance_before", "balance_after", "current_balance", "ducky_coins"}
        )

    def test_transaction_has_no_xp_fields(self):
        self.assertFalse(any("xp" in field.name.lower() for field in Transaction._meta.fields))

    def test_standard_orm_filters(self):
        reward = self.create_transaction(TransactionType.REWARD, 10)
        purchase = self.create_transaction(TransactionType.PURCHASE, -5)
        credit = self.create_transaction(TransactionType.ADJUSTMENT, 3)
        debit = self.create_transaction(TransactionType.ADJUSTMENT, -2)

        other_user = get_user_model().objects.create_user(
            username="other_transaction_user"
        )
        other_wallet = Wallet.objects.create(user=other_user)

        Transaction.objects.create(
            wallet=other_wallet,
            transaction_type=TransactionType.REWARD,
            amount=20,
        )

        self.assertEqual(
            list(
                self.wallet.transactions.filter(
                    transaction_type=TransactionType.PURCHASE
                )
            ),
            [purchase],
        )

        self.assertEqual(
            list(
                self.wallet.transactions.filter(
                    transaction_type=TransactionType.REWARD
                )
            ),
            [reward],
        )

        self.assertCountEqual(
            self.wallet.transactions.filter(amount__gt=0),
            [reward, credit],
        )

        self.assertCountEqual(
            self.wallet.transactions.filter(amount__lt=0),
            [purchase, debit],
        )

        self.assertCountEqual(
            Transaction.objects.filter(wallet__user=self.user),
            [reward, purchase, credit, debit],
        )
