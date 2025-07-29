import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barter_platform.settings')
django.setup()

from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from ads.models import Ad
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

User = get_user_model()


class AdModelTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.valid_ad_data = {
            'user': self.user,
            'title': 'Тестовое объявление',
            'description': 'Описание тестового объявления',
            'category': 'электроника',
            'condition': 'новое'
        }

    def test_ad_creation(self):
        """Проверка создания объявления"""
        ad = Ad.objects.create(**self.valid_ad_data)
        self.assertEqual(ad.title, 'Тестовое объявление')
        self.assertEqual(ad.user.username, 'testuser')

    def test_ad_str_method(self):
        """Проверка строкового представления"""
        ad = Ad.objects.create(**self.valid_ad_data)
        self.assertEqual(str(ad), 'Тестовое объявление')

    def test_missing_required_fields(self):
        """Проверка валидации обязательных полей"""
        # Тестируем отсутствие пользователя
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Ad.objects.create(
                    title='Без пользователя',
                    description='Описание',
                    category='электроника',
                    condition='новое'
                )

        with self.assertRaises(ValidationError):
            ad = Ad(
                user=self.user,
                description='Описание без заголовка',
                category='электроника',
                condition='новое'
            )
            ad.full_clean()
