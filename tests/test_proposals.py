import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barter_platform.settings')
django.setup()

from django.test import TestCase
from ads.models import Ad, ExchangeProposal
from django.contrib.auth import get_user_model

User = get_user_model()


class ExchangeProposalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='test123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='test123'
        )
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Ноутбук',
            description='Мощный ноутбук',
            category='электроника',
            condition='б/у'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Телефон',
            description='Смартфон',
            category='электроника',
            condition='новое'
        )

    def test_proposal_creation(self):
        """Создание предложения обмена"""
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Предлагаю обмен'
        )
        self.assertEqual(proposal.status, 'pending')
        self.assertEqual(proposal.comment, 'Предлагаю обмен')

    def test_proposal_status_change(self):
        """Изменение статуса предложения"""
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2
        )
        proposal.status = 'accepted'
        proposal.save()
        self.assertEqual(proposal.get_status_display(), 'Принята')
