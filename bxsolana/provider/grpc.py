import os
from typing import Optional

from grpclib import client
from solders import keypair as kp

from .. import transaction
from . import constants
from .base import Provider
from .package_info import NAME, VERSION


class GrpcProvider(Provider):
    # pyre-ignore[15]: overriding to force context manager hooks
    channel: Optional[client.Channel] = None

    _host: str
    _port: int
    _auth_header: str
    _use_ssl: bool
    _private_key: Optional[kp.Keypair]

    def __init__(
        self,
        host: str = constants.MAINNET_API_NY_GRPC_HOST,
        port: int = constants.MAINNET_API_GRPC_PORT,
        private_key: Optional[str] = None,
        auth_header: Optional[str] = None,
        use_ssl: bool = False,
        *,
        timeout: Optional[float] = None,
    ):
        self._host = host
        self._port = port
        self._use_ssl = use_ssl

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

        super().__init__(
            # pyre-ignore[6]: overriding to force context manager hooks
            None,
            timeout=timeout,
        )

    async def connect(self):
        if self.channel is None:
            self.channel = client.Channel(
                self._host, self._port, ssl=self._use_ssl
            )
            self.metadata = {
                "authorization": self._auth_header,
                "x-sdk": NAME,
                "s-sdk-version": VERSION,
            }

    def private_key(self) -> Optional[kp.Keypair]:
        return self._private_key

    async def close(self):
        channel = self.channel
        if channel is not None:
            self.channel.close()


def grpc(auth_header: Optional[str] = None) -> Provider:
    return GrpcProvider(auth_header=auth_header, use_ssl=True)


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
