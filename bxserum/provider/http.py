from typing import Type, AsyncGenerator

from bxserum.provider.base import Provider, T


class HttpProvider(Provider):
    endpoint: str

    def __init__(self, ip: str, port: int):
        self.endpoint = f"http://{ip}:{port}"

    async def request(
        self, route: str, request: "IProtoMessage", response_type: Type[T]
    ) -> T:
        async with 


    async def stream(
        self, route: str, request: "IProtoMessage", response_type: Type[T]
    ) -> AsyncGenerator[T, None]:
        raise NotImplementedError("streams are not supported on http")
