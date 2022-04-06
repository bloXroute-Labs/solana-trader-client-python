from typing import TYPE_CHECKING, Optional

from grpclib import client

from bxserum.provider.base import Provider

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import _MetadataLike, Deadline


class GrpcProvider(Provider):
    def __init__(
        self,
        ip: str,
        port: int,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ):
        channel = client.Channel(ip, port)
        super().__init__(channel, timeout=timeout, deadline=deadline, metadata=metadata)

    def close(self):
        self.channel.close()
