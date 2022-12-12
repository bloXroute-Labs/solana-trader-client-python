from abc import ABC, abstractmethod
from typing import List, Optional

from solana import keypair
from bxsolana_trader_proto import api
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
        side: "api.Side",
        types: List["api.OrderType"],
        amount: float,
        price: float,
        open_orders_address: str = "",
        client_order_id: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = False,
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
            project=project,
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            transaction=signed_tx, skip_pre_flight=skip_pre_flight
        )
        return result.signature

    async def submit_cancel_order(
        self,
        order_i_d: str = "",
        side: api.Side = api.Side.S_UNKNOWN,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_cancel_order(
            order_i_d=order_i_d,
            side=side,
            market_address=market_address,
            owner_address=owner_address,
            open_orders_address=open_orders_address,
            project=project,
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            transaction=signed_tx, skip_pre_flight=skip_pre_flight
        )
        return result.signature

    async def submit_cancel_by_client_order_i_d(
        self,
        client_order_i_d: int = 0,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_cancel_by_client_order_i_d(
            client_order_i_d=client_order_i_d,
            market_address=market_address,
            owner_address=owner_address,
            open_orders_address=open_orders_address,
            project=project,
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            transaction=signed_tx, skip_pre_flight=skip_pre_flight
        )
        return result.signature

    async def submit_cancel_all(
        self,
        market: str = "",
        owner_address: str = "",
        open_orders_addresses: Optional[List[str]] = None,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> List[str]:
        if open_orders_addresses is None:
            open_orders_addresses = []

        pk = self.require_private_key()
        response = await self.post_cancel_all(
            market=market,
            owner_address=owner_address,
            open_orders_addresses=open_orders_addresses,
            project=project,
        )

        signatures = []
        for tx in response.transactions:
            signed_tx = transaction.sign_tx_message_with_private_key(tx, pk)
            result = await self.post_submit(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
            signatures.append(result.signature)

        return signatures

    async def submit_settle(
        self,
        owner_address: str = "",
        market: str = "",
        base_token_wallet: str = "",
        quote_token_wallet: str = "",
        open_orders_address: str = "",
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = False,
    ) -> str:
        pk = self.require_private_key()
        response = await self.post_settle(
            owner_address=owner_address,
            market=market,
            base_token_wallet=base_token_wallet,
            quote_token_wallet=quote_token_wallet,
            open_orders_address=open_orders_address,
            project=project,
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            response.transaction, pk
        )
        result = await self.post_submit(
            transaction=signed_tx, skip_pre_flight=skip_pre_flight
        )
        return result.signature

    async def submit_replace_by_client_order_i_d(
        self,
        owner_address: str,
        payer_address: str,
        market: str,
        side: "api.Side",
        types: List["api.OrderType"],
        amount: float,
        price: float,
        open_orders_address: str = "",
        client_order_i_d: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = False,
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_replace_by_client_order_i_d(
            owner_address=owner_address,
            payer_address=payer_address,
            market=market,
            side=side,
            type=types,
            amount=amount,
            price=price,
            open_orders_address=open_orders_address,
            client_order_i_d=client_order_i_d,
            project=project,
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            transaction=signed_tx, skip_pre_flight=skip_pre_flight
        )
        return result.signature

    async def submit_replace_order(
        self,
        order_i_d: str,
        owner_address: str,
        payer_address: str,
        market: str,
        side: "api.Side",
        types: List["api.OrderType"],
        amount: float,
        price: float,
        open_orders_address: str = "",
        client_order_id: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = False,
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_replace_order(
            owner_address=owner_address,
            payer_address=payer_address,
            market=market,
            side=side,
            type=types,
            amount=amount,
            price=price,
            open_orders_address=open_orders_address,
            client_order_i_d=client_order_id,
            order_i_d=order_i_d,
            project=project,
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            transaction=signed_tx, skip_pre_flight=skip_pre_flight
        )
        return result.signature


class NotConnectedException(Exception):
    pass
