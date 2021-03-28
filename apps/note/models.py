from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Note(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='автор',
    )
    title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='название',
    )
    text = models.TextField(verbose_name='текст')
    is_public = models.BooleanField(default=False, verbose_name='публичная заметка')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('note', args=(self.id,))

    def __str__(self) -> str:
        is_public = 'public' if self.is_public else 'private'
        parts = (str(self.id), self.author.get_full_name(), self.title, is_public)
        return ' | '.join(part for part in parts if part)
