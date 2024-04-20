from __future__ import annotations

from enum import StrEnum, auto

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field
from pyrsistent import PMap, pmap, ny

from .model import (
    Channel,
    ChannelNotFoundError,
    DuplicateUserError,
    Message,
    User,
    UserAddData,
    UserNotFoundError
)


class AppActionType(StrEnum):
    ADD_MESSAGE = auto()
    ADD_USER = auto()
    CLEAN_UP_CHANNELS = auto()
    REMOVE_USER = auto()


class AddMessageAction(BaseModel):
    type: Annotated[
        Literal[AppActionType.ADD_MESSAGE],
        Field(default=AppActionType.ADD_MESSAGE)
    ]

    channel_name: str
    message: Message


class AddUserAction(BaseModel):
    type: Annotated[
        Literal[AppActionType.ADD_USER],
        Field(default=AppActionType.ADD_USER)
    ]

    data: UserAddData


class RemoveUserAction(BaseModel):
    type: Annotated[
        Literal[AppActionType.REMOVE_USER],
        Field(default=AppActionType.REMOVE_USER)
    ]

    session_id: str


class CleanUpChannelsAction(BaseModel):
    type: Annotated[
        Literal[AppActionType.CLEAN_UP_CHANNELS],
        Field(default=AppActionType.CLEAN_UP_CHANNELS)
    ]


AppAction = Annotated[
    Union[
        AddMessageAction,
        AddUserAction,
        CleanUpChannelsAction,
        RemoveUserAction
    ],
    Field(discriminator="type")
]


class AppState(BaseModel, frozen=True):
    channels: Annotated[PMap[str, Channel], Field(default_factory=pmap)]
    users: Annotated[PMap[str, User], Field(default_factory=pmap)]

    def add_message(self, channel_name: str, message: Message) -> AppState:
        channel = self \
            .get_channel(channel_name) \
            .append_message(message)

        return self.copy(
            update={
                "channels": self.channels.set(channel_name, channel)
            }
        )

    def add_user(self, data: UserAddData) -> AppState:
        if data.session_id in self.users:
            raise DuplicateUserError

        if data.channel_name in self.channels:
            channel = self.channels[data.channel_name]

            if data.name in channel.users:
                raise DuplicateUserError
        else:
            channel = Channel(name=data.channel_name)

        user = User(**data.dict())
        channel = channel.set_user(data.name, user)

        return AppState(
            channels=self.channels.set(data.channel_name, channel),
            users=self.users.set(data.session_id, user)
        )

    def clean_up_channels(self) -> AppState:
        channels = self.channels.transform(
            [ny],
            lambda channel: channel.discard_users()
        )

        return self.copy(
            update={
                "channels": channels
            }
        )

    def get_channel(self, name: str) -> Channel:
        if name not in self.channels:
            raise ChannelNotFoundError

        return self.channels[name]

    def get_user(self, session_id: str) -> User:
        if session_id not in self.users:
            raise UserNotFoundError

        return self.users[session_id]

    def remove_user(self, session_id: str) -> AppState:
        user = self.get_user(session_id)
        users = self.users.discard(session_id)

        channel = self.channels[user.channel_name] \
            .discard_user(user.name)

        channels = self.channels.set(user.channel_name, channel)

        return AppState(channels=channels, users=users)


def app_reducer(state: AppState, action: AppAction) -> AppState:
    match action:
        case AddMessageAction(channel_name=channel_name, message=message):
            return state.add_message(channel_name, message)

        case AddUserAction(data=data):
            return state.add_user(data)

        case CleanUpChannelsAction():
            return state.clean_up_channels()

        case RemoveUserAction(session_id=session_id):
            return state.remove_user(session_id)

        case _:
            raise TypeError(f"Unknown action: {action.type}")
