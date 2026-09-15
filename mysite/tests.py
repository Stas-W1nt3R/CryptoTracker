from django.test import TestCase
import unittest
from .models import TgUser, Cryptocurrency, UserTracking
from django.db.utils import IntegrityError


class CreateUser(TestCase):
    def setUp(self):
        self.user = TgUser.objects.create(telegram_id=123, username='test123')
        self.cryptocurrency = Cryptocurrency.objects.create(name='Bitcoin',coin_id='bitcoin',price=75000)
        self.tracking = UserTracking.objects.create(user=self.user,  target_price=79000,cryptocurrency=self.cryptocurrency)

    def test_create_user(self):
        user = TgUser.objects.get(username='test123')
        self.assertEqual(user.username, self.user.username)
        self.assertEqual(user.telegram_id, self.user.telegram_id)

    def test_create_cryptocurrency(self):
        cryptocurrency = Cryptocurrency.objects.get(name='Bitcoin')
        self.assertEqual(cryptocurrency.name, self.cryptocurrency.name)
        self.assertEqual(cryptocurrency.coin_id, self.cryptocurrency.coin_id)
        self.assertEqual(cryptocurrency.price, self.cryptocurrency.price)

    def test_create_tracking(self):
        tracking, created = UserTracking.objects.get_or_create(user=self.user, cryptocurrency=self.cryptocurrency,defaults={'target_price': 79000})
        self.assertEqual(tracking.user, self.user)
        self.assertEqual(tracking.target_price, self.tracking.target_price)
        self.assertEqual(tracking.cryptocurrency, self.tracking.cryptocurrency)

    def test_is_active_true(self):
        self.assertTrue(self.tracking.is_active)

    def test_create_duplicate_user(self):
        with self.assertRaises(IntegrityError):
            TgUser.objects.create(telegram_id=123,username='test123')

    def test_create_duplicate_cryptocurrency(self):
        with self.assertRaises(IntegrityError):
            Cryptocurrency.objects.create(name='Bitcoin',coin_id='bitcoin',price=75000)

    def test_create_duplicate_tracking(self):
        with self.assertRaises(IntegrityError):
            UserTracking.objects.create(user=self.user, target_price=80000,cryptocurrency=self.cryptocurrency)
