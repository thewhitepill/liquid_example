import redis.asyncio

from fastapi import FastAPI, WebSocket

from fastapi.middleware.cors import CORSMiddleware
from liquid import create_store, apply_middleware
from liquid_redis import redis_store_factory

from .config import config
from .middleware import WebsocketClientConnectAction, websocket_middleware
from .state import AppState, CleanUpChannelsAction, app_reducer


redis_client = redis.asyncio.from_url(config.redis.url)
store = create_store(
    app_reducer,
    AppState(),
    enhancer=apply_middleware(websocket_middleware),
    factory=redis_store_factory
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "CONNECT",
        "OPTIONS",
        "TRACE",
        "PATCH"
    ],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin"
    ]
)


@app.on_event("startup")
async def handle_startup() -> None:
    await redis_client.ping()
    await store.bind(redis_client, config.redis.namespace)
    await store.dispatch(CleanUpChannelsAction())


@app.on_event("shutdown")
async def handle_shutdown() -> None:
    await store.unbind()
    await redis_client.close()


@app.websocket("/channels/{channel_name}/users/{user_name}")
async def connect(
    client: WebSocket,
    channel_name: str,
    user_name: str
) -> None:
    await store.dispatch(
        WebsocketClientConnectAction(
            client=client,
            channel_name=channel_name,
            user_name=user_name
        )
    )
