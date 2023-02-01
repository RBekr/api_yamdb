from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Title(models.Model):
    pass


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        null=True
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    score = models.TextField(
        verbose_name='в работе'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    pass
