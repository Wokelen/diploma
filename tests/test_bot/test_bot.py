from unittest.mock import patch

import pytest
from rest_framework import status

from bot.models import TgUser
from bot.tg.client import TgClient


@pytest.mark.django_db()
class TestBot:

    @patch.object(TgClient, 'send_message')
    def test_bot_request(self, mocked_send_message, auth_client, tg_user_factory, user):
        tg_user = tg_user_factory.create(user=None, verification_code='code')
        # tg_user.update_verification_code()

        response = auth_client.patch('/bot/verify', data={'verification_code': 'code'})

        assert response.status_code == status.HTTP_200_OK
        mocked_send_message.assert_called_once_with(chat_id=tg_user.chat_id, text='Пользователь верифицирован')
        tg_user.refresh_from_db()
        assert tg_user.user == user
