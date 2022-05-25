import threading
from threading import Lock
from typing import AsyncGenerator, Optional, Awaitable, Type, Union
from types import TracebackType

import aiohttp

from bxserum.provider.wsrpc import JsonRpcRequest, JsonRpcResponse


class WSStreamManager():
    _ws: Optional[aiohttp.ClientWebSocketResponse] = None
    _subscription_manager: dict[str, AsyncGenerator]
    _lock: Lock

    def __init__(self, ws: aiohttp.ClientWebSocketResponse):
        self._ws = ws
        self._subscription_manager = {}
        self._lock = threading.Lock()

    async def run(self):
        #resp: JsonRpcResponse
        print("here 2")
        async for resp in self._ws:
            print("here 3")
            print(resp)
            if resp.id in self._subscription_manager:
                generator = self._subscription_manager[resp.id]
                await generator.asend(resp)

    async def __anext__(self):
        return await self._ws.__anext__()

    def __aiter__(self):
        return self._ws.__aiter__()

    def _add(self, request_id: str) -> Optional[AsyncGenerator]:
        self._lock.acquire()

        if request_id in self._subscription_manager:
            return None
        generator = WSAsyncGenerator(request_id, self)
        self._subscription_manager[request_id] = generator

        self._lock.release()
        return generator

    def _remove(self, request_id: str) -> Optional[AsyncGenerator]:
        self._lock.acquire()

        if request_id not in self._subscription_manager:
            return None
        generator = self._subscription_manager[request_id]
        del self._subscription_manager[request_id]

        self._lock.release()
        return generator

    async def subscribe(self, request: JsonRpcRequest) -> Optional[AsyncGenerator]:
        if request.id == None or request.id in self._subscription_manager:
            raise Exception()

        await self._ws.send_json(request.to_json())
        generator = self._add(request.id)
        if not generator:
            return None

        return generator

    async def unsubscribe(self, request_id: str) -> Optional[AsyncGenerator]:
        return self._remove(request_id)

        # create a subscription id
        # get subscription id from response (will the api know that the subscription is already acquired?)
        # if subscription id is not in the manager, add it
        # keep looking for any responses with the id and if it matches, then send them here
            # but what do we do with requests that are not the id?
            # maybe start this in the __init__.py?

class WSAsyncGenerator(AsyncGenerator):
    request_id: str
    stream_manager: WSStreamManager

    def __init__(self, request_id: str, stream_manager: WSStreamManager):
        self.request_id = request_id
        self.stream_manager = stream_manager

    async def __aexit__(self) -> Optional[AsyncGenerator]:
        return await self.stream_manager.unsubscribe(request_id=self.request_id)

    async def __anext__(self):
        return await self.stream_manager.__anext__()

    def __aiter__(self):
        return self.stream_manager.__aiter__()

    def asend(self, __value) -> Awaitable:
        pass

    def athrow(
        self, __typ: Type[BaseException], __val: Union[BaseException, object] = ..., __tb: Optional[TracebackType] = ...
    ) -> Awaitable:
        pass