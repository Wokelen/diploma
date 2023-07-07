import factory
from pytest_factoryboy import register

from bot.models import TgUser


@register
class TgUserFactory(factory.django.DjangoModelFactory):
    chat_id = factory.Faker('random_int', min=1)

    class Meta:
        model = TgUser
