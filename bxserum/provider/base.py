from abc import ABC, abstractmethod
from typing import List, Optional

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
    def private_key(self) -> Optional[keypair.Keypair]:
        pass

    @abstractmethod
    async def close(self):
        pass

    def require_private_key(self) -> keypair.Keypair:
        kp = self.private_key()
        if kp is None:
            raise EnvironmentError("private key has not been set in provider")
        return kp

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
        pk = self.require_private_key()
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
        signed_tx = transaction.sign_tx_with_private_key(order.transaction, pk)
        result = await self.post_submit(transaction=signed_tx)
        return result.signature

    async def submit_cancel_order(
        self,
        order_i_d: str = "",
        side: "proto.Side" = 0,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_cancel_order(
            order_i_d=order_i_d,
            side=side,
            market_address=market_address,
            owner_address=owner_address,
            open_orders_address=open_orders_address,
        )
        signed_tx = transaction.sign_tx_with_private_key(order.transaction, pk)
        result = await self.post_submit(transaction=signed_tx, skip_pre_flight=True)
        return result.signature

    async def submit_cancel_by_client_order_i_d(
        self,
        client_order_i_d: int = 0,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_cancel_by_client_order_i_d(
            client_order_i_d=client_order_i_d,
            market_address=market_address,
            owner_address=owner_address,
            open_orders_address=open_orders_address,
        )
        signed_tx = transaction.sign_tx_with_private_key(order.transaction, pk)
        result = await self.post_submit(transaction=signed_tx, skip_pre_flight=True)
        return result.signature


class NotConnectedException(Exception):
    pass
