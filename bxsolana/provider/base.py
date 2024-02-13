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

    async def submit_order(
        self,
        owner_address: str,
        payer_address: str,
        market: str,
        side: "api.Side",
        types: List["OrderType"],
        amount: float,
        price: float,
        open_orders_address: str = "",
        client_order_id: int = 0,
        compute_limit: int = 0,
        compute_price: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_order(
            post_order_request=api.PostOrderRequest(
                owner_address=owner_address,
                payer_address=payer_address,
                market=market,
                side=side,
                type=types,
                amount=amount,
                price=price,
                open_orders_address=open_orders_address,
                client_order_id=client_order_id,
                compute_limit=compute_limit,
                compute_price=compute_price,
                project=project,
            )
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )
        return result.signature

    async def submit_cancel_order(
        self,
        order_id: str = "",
        side: api.Side = api.Side.S_UNKNOWN,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
        compute_limit: int = 0,
        compute_price: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_cancel_order(
            post_cancel_order_request=api.PostCancelOrderRequest(
                order_id=order_id,
                side=side,
                market_address=market_address,
                owner_address=owner_address,
                open_orders_address=open_orders_address,
                compute_limit=compute_limit,
                compute_price=compute_price,
                project=project,
            )
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )
        return result.signature

    async def submit_cancel_by_client_order_id(
        self,
        client_order_id: int = 0,
        market_address: str = "",
        owner_address: str = "",
        open_orders_address: str = "",
        compute_limit: int = 0,
        compute_price: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()

        order = await self.post_cancel_by_client_order_id(
            post_cancel_by_client_order_id_request=api.PostCancelByClientOrderIdRequest(
                client_order_id=client_order_id,
                market_address=market_address,
                owner_address=owner_address,
                open_orders_address=open_orders_address,
                compute_limit=compute_limit,
                compute_price=compute_price,
                project=project,
            )
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )
        return result.signature

    async def submit_cancel_all(
        self,
        market: str = "",
        owner_address: str = "",
        open_orders_addresses: Optional[List[str]] = None,
        compute_limit: int = 0,
        compute_price: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> List[str]:
        if open_orders_addresses is None:
            open_orders_addresses = []

        pk = self.require_private_key()
        response = await self.post_cancel_all(
            post_cancel_all_request=api.PostCancelAllRequest(
                market=market,
                owner_address=owner_address,
                open_orders_addresses=open_orders_addresses,
                compute_limit=compute_limit,
                compute_price=compute_price,
                project=project,
            )
        )

        signatures = []
        for tx in response.transactions:
            signed_tx = transaction.sign_tx_message_with_private_key(tx, pk)
            result = await self.post_submit(
                post_submit_request=api.PostSubmitRequest(
                    transaction=signed_tx, skip_pre_flight=skip_pre_flight
                )
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
        compute_limit: int = 0,
        compute_price: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        response = await self.post_settle(
            post_settle_request=api.PostSettleRequest(
                owner_address=owner_address,
                market=market,
                base_token_wallet=base_token_wallet,
                quote_token_wallet=quote_token_wallet,
                open_orders_address=open_orders_address,
                compute_limit=compute_limit,
                compute_price=compute_price,
                project=project,
            )
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            response.transaction, pk
        )
        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )
        return result.signature

    async def submit_replace_by_client_order_id(
        self,
        owner_address: str,
        payer_address: str,
        market: str,
        side: "api.Side",
        types: List["OrderType"],
        amount: float,
        price: float,
        open_orders_address: str = "",
        client_order_id: int = 0,
        compute_limit: int = 0,
        compute_price: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_replace_by_client_order_id(
            post_order_request=api.PostOrderRequest(
                owner_address=owner_address,
                payer_address=payer_address,
                market=market,
                side=side,
                type=types,
                amount=amount,
                price=price,
                open_orders_address=open_orders_address,
                client_order_id=client_order_id,
                compute_limit=compute_limit,
                compute_price=compute_price,
                project=project,
            )
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )
        return result.signature

    async def submit_replace_order(
        self,
        order_id: str,
        owner_address: str,
        payer_address: str,
        market: str,
        side: "api.Side",
        types: List["OrderType"],
        amount: float,
        price: float,
        open_orders_address: str = "",
        client_order_id: int = 0,
        compute_limit: int = 0,
        compute_price: int = 0,
        project: api.Project = api.Project.P_UNKNOWN,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        order = await self.post_replace_order(
            post_replace_order_request=api.PostReplaceOrderRequest(
                owner_address=owner_address,
                payer_address=payer_address,
                market=market,
                side=side,
                type=types,
                amount=amount,
                price=price,
                open_orders_address=open_orders_address,
                client_order_id=client_order_id,
                order_id=order_id,
                compute_limit=compute_limit,
                compute_price=compute_price,
                project=project,
            )
        )
        signed_tx = transaction.sign_tx_message_with_private_key(
            order.transaction, pk
        )
        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )
        return result.signature

    async def submit_post_trade_swap(
        self,
        *,
        project: api.Project = api.Project.P_UNKNOWN,
        owner_address: str = "",
        in_token: str = "",
        out_token: str = "",
        in_amount: float = 0,
        slippage: float = 0,
        compute_limit: int = 0,
        compute_price: int = 0,
        skip_pre_flight: bool = True,
        submit_strategy: api.SubmitStrategy = api.SubmitStrategy.P_ABORT_ON_FIRST_ERROR,
    ) -> api.PostSubmitBatchResponse:
        pk = self.require_private_key()
        result = await self.post_trade_swap(
            trade_swap_request=api.TradeSwapRequest(
                project=project,
                owner_address=owner_address,
                in_token=in_token,
                out_token=out_token,
                in_amount=in_amount,
                slippage=slippage,
                compute_limit=compute_limit,
                compute_price=compute_price,
            )
        )

        signed_txs: List[api.PostSubmitRequestEntry] = []
        for tx in result.transactions:
            signed_tx = transaction.sign_tx_message_with_private_key(tx, pk)
            signed_txs.append(
                api.PostSubmitRequestEntry(
                    transaction=signed_tx, skip_pre_flight=skip_pre_flight
                )
            )

        return await self.post_submit_batch(
            post_submit_batch_request=api.PostSubmitBatchRequest(
                entries=signed_txs, submit_strategy=submit_strategy
            )
        )

    async def submit_post_route_trade_swap(
        self,
        *,
        project: api.Project = api.Project.P_UNKNOWN,
        owner_address: str = "",
        steps: List["api.RouteStep"] = [],
        slippage: float = 0,
        compute_limit: int = 0,
        compute_price: int = 0,
        skip_pre_flight: bool = True,
        submit_strategy: api.SubmitStrategy = api.SubmitStrategy.P_ABORT_ON_FIRST_ERROR,
    ) -> api.PostSubmitBatchResponse:
        pk = self.require_private_key()
        result = await self.post_route_trade_swap(
            route_trade_swap_request=api.RouteTradeSwapRequest(
                project=project,
                owner_address=owner_address,
                steps=steps,
                slippage=slippage,
                compute_limit=compute_limit,
                compute_price=compute_price,
            )
        )

        signed_txs: List[api.PostSubmitRequestEntry] = []
        for tx in result.transactions:
            signed_tx = transaction.sign_tx_message_with_private_key(tx, pk)
            signed_txs.append(
                api.PostSubmitRequestEntry(
                    transaction=signed_tx, skip_pre_flight=skip_pre_flight
                )
            )

        return await self.post_submit_batch(
            post_submit_batch_request=api.PostSubmitBatchRequest(
                entries=signed_txs, submit_strategy=submit_strategy
            )
        )


class NotConnectedException(Exception):
    pass
