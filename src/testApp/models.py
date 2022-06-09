from django.db import models

# Create your models here.
class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID пользователя в сети',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя'
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(
        to='testApp.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Сообщение {self.pk} от  {self.profile}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class UserSHA(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='User ID',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Username',
        unique=True,
    )
    user_sha = models.TextField(
        verbose_name='User token',
        unique=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Auth time',
        auto_now_add=True,
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'User SHA'
        verbose_name_plural = 'Users SHA'
