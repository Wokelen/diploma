from typing import Optional
import requests
from requests import Response

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from todolist.settings import TG_TOKEN


class TgClient:
    """
    The TgClient class contains all the necessary methods for working with the telegram bot API.
    """
    def __init__(self, token: Optional[str] = None) -> None:
        """
        The __init__ function is called when creating an instance of the TgClient class. Accepts as parameters
        the value of the telegram bot token or uses the token from the application settings.
        """
        self.token = token if token else TG_TOKEN

    def get_url(self, method: str) -> str:
        """
        The get_url function defines a class method. Accepts as parameters the name of the method of interaction
        with the telegram API in the form of a string. Returns the URL for making the request as a string.
        """
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """
        The get_updates function defines a class method. Accepts offset and timeout as parameters with certain
        values by omission. Produces a telegram API request for sent messages. Returns the API response
        as a GetUpdatesResponse object.
        """
        url: str = self.get_url("getUpdates")
        response: Response = requests.get(url, params={"offset": offset, "timeout": timeout})
        return GetUpdatesResponse.Schema().load(response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """
        The send_message function defines a class method. Accepts chat_id as an integer and text as a string
        as parameters. Makes a POST request to the telegram API with sending a message to the specified chat.
        Returns the API response as a SendMessageResponse object.
        """
        url: str = self.get_url("sendMessage")
        response: Response = requests.post(url, params={"chat_id": chat_id, "text": text})
        return SendMessageResponse.Schema().load(response.json())
