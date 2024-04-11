from enum import StrEnum, auto
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from .model import ChannelDisplayData, Message, UserDisplayData


class ServerMessageType(StrEnum):
    CHANNEL_STATE = auto()
    MESSAGE_BROADCAST = auto()
    USER_JOIN = auto()
    USER_LEAVE = auto()


class ClientMessageType(StrEnum):
    MESSAGE_SEND_REQUEST = auto()


class ChannelStateMessage(BaseModel):
    type: Annotated[
        Literal[ServerMessageType.CHANNEL_STATE],
        Field(default=ServerMessageType.CHANNEL_STATE)
    ]

    channel: ChannelDisplayData


class MessageBroadcastMessage(BaseModel):
    type: Annotated[
        Literal[ServerMessageType.MESSAGE_BROADCAST],
        Field(default=ServerMessageType.MESSAGE_BROADCAST)
    ]

    message: Message


class MessageSendRequestMessage(BaseModel):
    type: Annotated[
        Literal[ClientMessageType.MESSAGE_SEND_REQUEST],
        Field(default=ClientMessageType.MESSAGE_SEND_REQUEST)
    ]

    content: str


class UserJoinMessage(BaseModel):
    type: Annotated[
        Literal[ServerMessageType.USER_JOIN],
        Field(default=ServerMessageType.USER_JOIN)
    ]

    user: UserDisplayData


class UserLeaveMessage(BaseModel):
    type: Annotated[
        Literal[ServerMessageType.USER_LEAVE],
        Field(default=ServerMessageType.USER_LEAVE)
    ]

    user: UserDisplayData

ClientMessage = Annotated[
    Union[MessageSendRequestMessage],
    Field(default_factory=MessageSendRequestMessage, discriminator="type")
]


ServerMessage = Annotated[
    Union[
        ChannelStateMessage,
        MessageBroadcastMessage,
        UserJoinMessage,
        UserLeaveMessage
    ],
    Field(discriminator="type")
]
