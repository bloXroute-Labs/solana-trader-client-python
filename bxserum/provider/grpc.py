import os
from typing import TYPE_CHECKING, Optional

from grpclib import client
from solana import keypair

from .. import transaction
from . import constants
from .base import Provider

if TYPE_CHECKING:

    # noinspection PyUnresolvedReferences,PyProtectedMember
    # pyre-ignore[21]: module is too hard to find
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline


class GrpcProvider(Provider):
    # pyre-ignore[15]: overriding to force context manager hooks
    channel: Optional[client.Channel] = None

    _host: str
    _port: int
    _private_key: Optional[keypair.Keypair]

    def __init__(
        self,
        host: str = constants.MAINNET_API_GRPC_HOST,
        port: int = constants.MAINNET_API_GRPC_PORT,
        private_key: Optional[str] = None,
        auth_header: Optional[str] = None,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ):
        self._host = host
        self._port = port
        self._auth_header = auth_header

        if private_key is None:
            try:
                self._private_key = transaction.load_private_key_from_env()
            except EnvironmentError:
                self._private_key = None
        else:
            self._private_key = transaction.load_private_key(private_key)

        if auth_header is None:
            self._auth_header = os.environ["AUTH_HEADER"]
        else:
            self._auth_header = auth_header

        # pyre-ignore[6]: overriding to force context manager hooks
        super().__init__(None, timeout=timeout, deadline=deadline, metadata=metadata)

    async def connect(self):
        if self.channel is None:
            self.channel = client.Channel(self._host, self._port)
            self.metadata = {"authorization": self._auth_header}

    def private_key(self) -> Optional[keypair.Keypair]:
        return self._private_key

    async def close(self):
        channel = self.channel
        if channel is not None:
            self.channel.close()


def grpc(auth_header: Optional[str] = None) -> Provider:
    return GrpcProvider(auth_header=auth_header)


def grpc_testnet(auth_header: Optional[str] = None) -> Provider:
    return GrpcProvider(
        host=constants.TESTNET_API_GRPC_HOST,
        port=constants.TESTNET_API_GRPC_PORT,
        auth_header=auth_header,
    )


def grpc_devnet(auth_header: Optional[str] = None) -> Provider:
    return GrpcProvider(
        host=constants.DEVNET_API_GRPC_HOST,
        port=constants.DEVNET_API_GRPC_PORT,
        auth_header=auth_header,
    )


def grpc_local(auth_header: Optional[str] = None) -> Provider:
    return GrpcProvider(
        host=constants.LOCAL_API_GRPC_HOST,
        port=constants.LOCAL_API_GRPC_PORT,
        auth_header=auth_header,
    )
