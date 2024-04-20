from __future__ import annotations

import random

from typing import Annotated

from pydantic import BaseModel, Field
from pyrsistent import PMap, pmap


class AccessError(Exception):
    pass


class DuplicateEntityError(Exception):
    pass


class EntityNotFoundError(Exception):
    pass


class ChannelNotFoundError(EntityNotFoundError):
    pass


class DuplicateUserError(DuplicateEntityError):
    pass


class UserNotFoundError(EntityNotFoundError):
    pass


class Message(BaseModel, frozen=True):
    sender_name: str
    sender_color_id: int
    content: str


class UserAddData(BaseModel, frozen=True):
    name: str
    session_id: str
    channel_name: str


class UserDisplayData(BaseModel, frozen=True):
    name: str
    color_id: int


class User(BaseModel, frozen=True):
    session_id: str
    name: str
    channel_name: str
    color_id: Annotated[
        int,
        Field(default_factory=lambda: random.randrange(255))
    ]

    def display(self) -> UserDisplayData:
        return UserDisplayData(name=self.name, color_id=self.color_id)


class ChannelDisplayData(BaseModel, frozen=True):
    name: str
    users: tuple[UserDisplayData, ...]
    messages: tuple[Message, ...]


class Channel(BaseModel, frozen=True):
    name: str
    users: Annotated[PMap[str, User], Field(default_factory=pmap)]
    messages: Annotated[tuple[Message, ...], Field(default_factory=tuple)]

    def append_message(self, message: Message) -> Channel:
        return self.copy(
            update={
                "messages": (*self.messages, message)
            }
        )

    def discard_user(self, name: str) -> Channel:
        if name not in self.users:
            raise UserNotFoundError

        return self.copy(
            update={
                "users": self.users.discard(name)
            }
        )

    def discard_users(self) -> Channel:
        return self.copy(
            update={
                "users": pmap()
            }
        )

    def get_user(self, name: str) -> User:
        if name not in self.users:
            raise UserNotFoundError

        return self.users[name]

    def set_user(self, name, user: User) -> Channel:
        return self.copy(
            update={
                "users": self.users.set(name, user)
            }
        )

    def display(self) -> ChannelDisplayData:
        return ChannelDisplayData(
            name=self.name,
            users=tuple(user.display() for user in self.users.values()),
            messages=self.messages
        )
