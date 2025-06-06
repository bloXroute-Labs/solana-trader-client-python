import os
import warnings
from typing import Optional

from grpclib import client
from grpclib.config import Configuration
from solders import keypair as kp # pyre-ignore[21]: module is too hard to find

from .. import transaction
from . import constants
from .base import Provider
from .package_info import NAME, VERSION


class GrpcProvider(Provider):
    # pyre-ignore[15]: overriding to force context manager hooks
    channel: Optional[client.Channel] = None # pyre-ignore[11]: annotation

    _host: str # pyre-ignore[11]: annotation
    _port: int # pyre-ignore[11]: annotation
    _auth_header: str # pyre-ignore[11]: annotation
    _use_ssl: bool # pyre-ignore[11]: annotation
    _private_key: Optional[kp.Keypair] # pyre-ignore[11]: annotation

    def __init__(
        self,
        host: str = constants._HOSTS["ny"],
        port: int = constants.GRPC_PORT_INSECURE,
        private_key: Optional[str] = None,
        auth_header: Optional[str] = None,
        use_ssl: bool = False,
        *,
        timeout: Optional[float] = None,
    ):
        if use_ssl:
             warnings.warn(constants.WARNING_TLS_SLOWDOWN)
             
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
            config = Configuration(
                _keepalive_time=15.0,
                _keepalive_timeout=5.0,
                _keepalive_permit_without_calls=True,  # PermitWithoutStream equivalent
            )

            self.channel = client.Channel(
                self._host, self._port, ssl=self._use_ssl, config=config
            )
            self.metadata = {
                "authorization": self._auth_header,
                "x-sdk": NAME,
                "x-sdk-version": VERSION,
            }

    def private_key(self) -> Optional[kp.Keypair]:
        return self._private_key

    async def close(self):
        if self.channel is not None:
            self.channel.close()
            self.channel = None


def grpc(auth_header: Optional[str] = None, private_key: Optional[str] = None, region: Optional[constants.Region] = constants.Region.NY, secure: Optional[bool] = False) -> GrpcProvider:
    host, port = constants.get_grpc_endpoint(region, secure)
    return GrpcProvider(
        host=host,
        port=port,
        use_ssl=secure,
        private_key=private_key,
        auth_header=auth_header
    )

def grpc_pump_ny(auth_header: Optional[str] = None, private_key: Optional[str] = None, secure: Optional[bool] = False) -> Provider:
    host, port = constants.get_grpc_endpoint(constants.Region.NY, secure, pump=True)
    return GrpcProvider(
        host=host,
        port=port,
        auth_header=auth_header,
        private_key=private_key,
        use_ssl=secure,
    )

def grpc_pump_uk(auth_header: Optional[str] = None, private_key: Optional[str] = None, secure: Optional[bool] = False) -> Provider:
    host, port = constants.get_grpc_endpoint(constants.Region.UK, secure, pump=True)
    return GrpcProvider(
        host=host,
        port=port,
        auth_header=auth_header,
        private_key=private_key,
        use_ssl=secure,
    )


def grpc_testnet(auth_header: Optional[str] = None, private_key: Optional[str] = None, secure: Optional[bool] = False) -> Provider:
    host, port = constants.get_testnet_endpoint(constants.ConnectionType.GRPC, secure=secure)
    return GrpcProvider(
        host=host,
        port=port,
        auth_header=auth_header,
        private_key=private_key,
        use_ssl=secure
    )


def grpc_devnet(auth_header: Optional[str] = None, private_key: Optional[str] = None, secure: Optional[bool] = False) -> Provider:
    host, port = constants.get_devnet_endpoint(constants.ConnectionType.GRPC, secure=secure)
    return GrpcProvider(
        host=host,
        port=port,
        private_key=private_key,
        auth_header=auth_header,
        use_ssl=secure
    )


def grpc_local(auth_header: Optional[str] = None, private_key: Optional[str] = None) -> Provider:
    return GrpcProvider(
        host=constants.LOCAL_API_GRPC_HOST,
        port=constants.LOCAL_API_GRPC_PORT,
        private_key=private_key,
        auth_header=auth_header,
        use_ssl=False
    )
