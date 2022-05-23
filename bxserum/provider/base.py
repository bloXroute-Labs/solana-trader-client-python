from abc import ABC, abstractmethod
from typing import List

from solana import keypair

from bxserum import proto, transaction


class Provider(proto.ApiStub, ABC):
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *exc_info):
        await self.close()

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    def private_key(self) -> keypair.Keypair:
        pass

    @abstractmethod
    async def close(self):
        pass

    async def submit_order(
        self,
        owner_address: str,
        payer_address: str,
        market: str,
        side: "proto.Side",
        types: List["proto.OrderType"],
        amount: float,
        price: float,
        open_orders_address: str = "",
        client_order_id: int = 0,
    ) -> str:
        order = await self.post_order(
            owner_address=owner_address,
            payer_address=payer_address,
            market=market,
            side=side,
            type=types,
            amount=amount,
            price=price,
            open_orders_address=open_orders_address,
            client_order_i_d=client_order_id,
        )
        signed_tx = transaction.sign_tx_with_private_key(order.transaction, self.private_key())
        result = await self.post_submit(transaction=signed_tx)
        return result.signature


class NotConnectedException(Exception):
    pass
