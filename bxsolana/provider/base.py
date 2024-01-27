from abc import ABC, abstractmethod
from typing import List, Optional

from bxsolana_trader_proto import api
from bxsolana_trader_proto.common import OrderType
from solders import keypair as kp

from .. import transaction


class Provider(api.ApiStub, ABC):
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *exc_info):
        await self.close()

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    def private_key(self) -> Optional[kp.Keypair]:
        pass

    @abstractmethod
    async def close(self):
        pass

    def require_private_key(self) -> kp.Keypair:
        kp = self.private_key()
        if kp is None:
            raise EnvironmentError("private key has not been set in provider")
        return kp

class NotConnectedException(Exception):
    pass
