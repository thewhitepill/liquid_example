import asyncio
import secrets

from fastapi import WebSocket, WebSocketDisconnect

from .model import ChannelNotFoundError, Message, UserAddData
from .protocol import (
    ChannelStateMessage,
    MessageBroadcastMessage,
    MessageSendRequestMessage,
    UserJoinMessage,
    UserLeaveMessage
)

from .state import AddMessageAction, AddUserAction, RemoveUserAction


class WebsocketClientConnectAction:
    def __init__(
        self,
        client: WebSocket,
        channel_name: str,
        user_name: str
    ) -> None:
        self.client = client
        self.channel_name = channel_name
        self.user_name = user_name


def websocket_middleware(store):
    clients = {}

    async def unicast(session_id, message):
        await clients[session_id].send_text(message.model_dump_json())

    async def multicast(session_ids, message):
        futures = [unicast(session_id, message) for session_id in session_ids]
        await asyncio.gather(*futures)

    def get_peer_session_ids(current_session_id, channel):
        return [
            user.session_id for user in channel.users.values()
            if user.session_id != current_session_id
        ]

    async def handle_client_message(channel_name, user, protocol_message):
        content = protocol_message.content
        model_message = Message(
            sender_name=user.name,
            sender_color_id=user.color_id,
            content=content
        )

        state = await store.dispatch(
            AddMessageAction(
                channel_name=channel_name,
                message=model_message
            )
        )

        channel = state.get_channel(channel_name)
        session_ids = channel.users.keys()

        await multicast(
            session_ids,
            MessageBroadcastMessage(
                message=model_message
            )
        )

    async def handle_client_connect(client, channel_name, user_name):
        session_id = secrets.token_hex(32)
        user_data = UserAddData(
            session_id=session_id,
            name=user_name,
            channel_name=channel_name
        )

        state = await store.dispatch(AddUserAction(data=user_data))
        channel = state.get_channel(channel_name)
        user = channel.get_user(user_name)
        peer_session_ids = get_peer_session_ids(session_id, channel)

        await client.accept()
        clients[session_id] = client

        await unicast(
            session_id,
            ChannelStateMessage(channel=channel.display())
        )

        await multicast(
            peer_session_ids,
            UserJoinMessage(user=user.display())
        )

        return user

    async def handle_client_disconnect(channel_name, user):
        del clients[user.session_id]

        state = await store.dispatch(
            RemoveUserAction(session_id=user.session_id)
        )

        try:
            channel = state.get_channel(channel_name)
        except ChannelNotFoundError:
            return

        peer_session_ids = get_peer_session_ids(user.session_id, channel)

        await multicast(
            peer_session_ids,
            UserLeaveMessage(user=user.display())
        )

    def apply(next):
        async def dispatch(action):
            if not isinstance(action, WebsocketClientConnectAction):
                return await next(action)

            client = action.client
            channel_name = action.channel_name
            user_name = action.user_name

            user = await handle_client_connect(
                client,
                channel_name,
                user_name
            )

            try:
                while True:
                    data = await client.receive_json()
                    message = MessageSendRequestMessage.model_validate(data)

                    await handle_client_message(channel_name, user, message)
            except WebSocketDisconnect:
                await handle_client_disconnect(channel_name, user)

        return dispatch

    return apply
