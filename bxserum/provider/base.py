from abc import ABC, abstractmethod

from bxserum import proto


class Provider(proto.ApiStub, ABC):
    async def __aenter__(self):
        await self.connect()

    async def __aexit__(self, *exc_info):
        await self.close()

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def close(self):
        pass


class NotConnectedException(Exception):
    pass
