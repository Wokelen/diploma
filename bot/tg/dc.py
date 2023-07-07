from dataclasses import field

from marshmallow_dataclass import dataclass
from marshmallow import EXCLUDE, Schema
from typing import List, ClassVar, Type, Optional


@dataclass
class MessageFrom:
    """
    The Message From class is a dataclass and is intended for serialization and deserialization of the telegram API
    response and validation of the received data contained in the value of the 'from' key.
    """
    id: int
    is_bot: bool
    first_name: Optional[str]
    username: Optional[str]

    class Meta:
        """
        The Meta class is an auxiliary class and defines the behavior when receiving unknown parameters.
        """
        unknown = EXCLUDE


@dataclass
class Chat:
    """
    The Chat class is a dataclass and is intended for serialization and deserialization of the telegram API response
    and validation of the received data contained in the value of the 'chat' key.
    """
    id: int
    first_name: Optional[str]
    username: Optional[str]
    type: str

    class Meta:
        """
        The Meta class is an auxiliary class and defines the behavior when receiving unknown parameters.
        """
        unknown = EXCLUDE


@dataclass
class Message:
    """
    The Message class is a dataclass and is intended for serialization and deserialization of the telegram API
    response and validation of the received data contained in the value of the 'message' key.
    """
    message_id: int
    date: int
    text: Optional[str]
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat

    class Meta:
        """
        The Meta class is an auxiliary class and defines the behavior when receiving unknown parameters.
        """
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    """
    The UpdateObj class is a dataclass and is intended for serialization and deserialization of the telegram API
    response and validation of the received data contained in the value of each element of the update list.
    """
    update_id: int
    message: Message

    class Meta:
        """
        The Meta class is an auxiliary class and defines the behavior when receiving unknown parameters.
        """
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    """
    The GetUpdatesResponse class is a dataclass and is intended for serialization and deserialization
    of the telegram API response and validation of the received data.
    """
    ok: bool
    result: List[UpdateObj] = field(default_factory=list)

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        """
        The Meta class is an auxiliary class and defines the behavior when receiving unknown parameters.
        """
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    """
    The SendMessageResponse class is a dataclass and is intended for serialization and deserialization
    of the telegram API response and validation of the received data.
    """
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        """
        The Meta class is an auxiliary class and defines the behavior when receiving unknown parameters.
        """
        unknown = EXCLUDE
