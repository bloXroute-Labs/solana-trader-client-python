from typing import TYPE_CHECKING, Optional

from grpclib import client

from bxserum.provider.base import Provider

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline


class GrpcProvider(Provider):
    channel: Optional[client.Channel] = None

    _ip: str
    _port: int

    def __init__(
        self,
        ip: str,
        port: int,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ):
        self._ip = ip
        self._port = port
        super().__init__(None, timeout=timeout, deadline=deadline, metadata=metadata)

    async def connect(self):
        if self.channel is None:
            self.channel = client.Channel(self._ip, self._port)

    async def close(self):
        channel = self.channel
        if channel is not None:
            self.channel.close()
