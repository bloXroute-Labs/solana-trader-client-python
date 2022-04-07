from typing import TYPE_CHECKING, Optional

from grpclib import client

from bxserum.provider.base import Provider
from bxserum.provider.constants import DEFAULT_HOST, DEFAULT_GRPC_PORT

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline


class GrpcProvider(Provider):
    channel: Optional[client.Channel] = None

    _host: str
    _port: int

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_GRPC_PORT,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ):
        self._host = host
        self._port = port
        super().__init__(None, timeout=timeout, deadline=deadline, metadata=metadata)

    async def connect(self):
        if self.channel is None:
            self.channel = client.Channel(self._host, self._port)

    async def close(self):
        channel = self.channel
        if channel is not None:
            self.channel.close()
