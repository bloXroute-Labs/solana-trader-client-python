import dataclasses
import os
from typing import AsyncGenerator, Dict, Optional, TYPE_CHECKING, Type

import jsonrpc
from solders import keypair as kp
from stringcase import camelcase

from . import Provider, constants
from .. import transaction

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    # pyre-ignore[21]: module is too hard to find
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline, T


class WsProvider(Provider):
    _ws: jsonrpc.WsRpcConnection

    _endpoint: str
    _private_key: Optional[kp.Keypair]

    # noinspection PyMissingConstructor
    def __init__(
        self,
        endpoint: str = constants.MAINNET_API_WS,
        auth_header: Optional[str] = None,
        private_key: Optional[str] = None,
        request_timeout_s: Optional[int] = None,
    ):
        self._endpoint = endpoint

        if auth_header is None:
            auth_header = os.environ["AUTH_HEADER"]

        opts = jsonrpc.WsRpcOpts(
            headers={"authorization": auth_header},
            request_timeout_s=request_timeout_s,
        )
        self._ws = jsonrpc.WsRpcConnection(endpoint, opts)

        if private_key is None:
            try:
                self._private_key = transaction.load_private_key_from_env()
            except EnvironmentError:
                self._private_key = None
        else:
            self._private_key = transaction.load_private_key(private_key)

    async def connect(self):
        await self._ws.connect()

    def private_key(self) -> Optional[kp.Keypair]:
        return self._private_key

    async def close(self):
        await self._ws.close()

    async def _unary_unary(
        self,
        route: str,
        # pyre-ignore[11]: type is too hard to find
        request: "IProtoMessage",
        response_type: Type["T"],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ) -> "T":
        result = await self._ws.call(
            _ws_endpoint(route), request.to_dict(include_default_values=False)
        )
        response = _validated_response(result, response_type)
        return response

    async def _unary_stream(
        self,
        route: str,
        request: "IProtoMessage",
        response_type: Type["T"],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ) -> AsyncGenerator["T", None]:
        subscription_id = await self._ws.subscribe(
            _ws_endpoint(route), request.to_dict()
        )
        async for update in self._ws.notifications_for_id(subscription_id):
            response = _validated_response(update, response_type)
            yield response


def _ws_endpoint(route: str) -> str:
    return route.split("/")[-1]


def ws() -> Provider:
    return WsProvider()


def ws_testnet() -> Provider:
    return WsProvider(endpoint=constants.TESTNET_API_WS)


def ws_devnet() -> Provider:
    return WsProvider(endpoint=constants.DEVNET_API_WS)


def ws_local() -> Provider:
    return WsProvider(endpoint=constants.LOCAL_API_WS)


def _validated_response(response: Dict, response_type: Type["T"]) -> "T":
    if not isinstance(response, dict):
        raise Exception(f"response {response} was not a dictionary")

    if "message" in response:
        raise Exception(response["message"])

    message = response_type().from_dict(response)

    fields = list(dataclasses.fields(message))
    field_names = [field.name for field in fields]

    for field in field_names:
        if camelcase(field) not in response:
            raise Exception(
                f"response {response} was not of type {response_type}"
            )

    return message
