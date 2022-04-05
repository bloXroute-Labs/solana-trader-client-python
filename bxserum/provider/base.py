from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type, TypeVar, Optional, AsyncGenerator

import betterproto

from bxserum import proto

if TYPE_CHECKING:
    from grpclib._protocols import IProtoMessage
    from betterproto import _MetadataLike, Deadline

T = TypeVar("T", bound=betterproto.Message)


class Provider(ABC):
    @abstractmethod
    async def request(
        self, route: str, request: "IProtoMessage", response_type: Type[T]
    ):
        pass

    @abstractmethod
    async def stream(
        self, route: str, request: "IProtoMessage", response_type: Type[T]
    ):
        pass


class ApiWrapper(proto.ApiStub):
    _provider: Provider

    # noinspection PyMissingConstructor
    def __init__(self, provider: Provider):
        self._provider = provider

    async def _unary_unary(
        self,
        route: str,
        request: "IProtoMessage",
        response_type: Type[T],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ) -> T:
        return await self._provider.request(route, request, response_type)

    async def _unary_stream(
        self,
        route: str,
        request: "IProtoMessage",
        response_type: Type[T],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["_MetadataLike"] = None,
    ) -> AsyncGenerator[T, None]:
        return await self._provider.stream(route, request, response_type)
