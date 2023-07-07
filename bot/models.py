from django.db import models
from django.utils.crypto import get_random_string

from core.models import User


class TgUser(models.Model):

    chat_id = models.BigIntegerField(primary_key=True, editable=False, verbose_name='Чат ID')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user_ud = models.BigIntegerField(null=True, blank=True, default=None)
    username = models.CharField(max_length=150, verbose_name='tg username', null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:

        return f'{self.__class__.__name__} {self.chat_id}'

    def update_verification_code(self) -> None:

        self.verification_code = self.generate_verification_code()
        self.save(update_fields=['verification_code'])

    @property
    def is_verified(self) -> bool:

        return bool(self.user)

    @staticmethod
    def generate_verification_code() -> str:

        return get_random_string(20)

