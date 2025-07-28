from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from .constants import (
    CATEGORY_CHOICES,
    CONDITION_CHOICES,
    STATUS_CHOICES
)

User = get_user_model()


class Ad(models.Model): 
    user = models.ForeignKey(
        User,
        related_name='ads',
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image_url = models.URLField('Ссылка на изображение', blank=True, null=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='другое'
    )

    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='б/у'
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='sent_proposals',
        verbose_name='Предложение от:'
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='received_proposals',
        verbose_name='Предложение для (объявление)'
    )
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField(
        'Статус',
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'

    def __str__(self):
        return f"Предложение #{self.id} ({self.get_status_display()})"
