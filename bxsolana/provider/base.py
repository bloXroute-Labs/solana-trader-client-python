from abc import ABC, abstractmethod
from typing import List, Optional

from bxsolana_trader_proto import api
from bxsolana_trader_proto.common import OrderType
from solders import keypair as kp     # pyre-ignore[21]: module is too hard to find

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
    def private_key(self) -> Optional[kp.Keypair]: # pyre-ignore[11]: annotation
        pass

    @abstractmethod
    async def close(self):
        pass

    def require_private_key(self) -> kp.Keypair:
        kp = self.private_key()
        if kp is None:
            raise EnvironmentError("private key has not been set in provider")
        return kp

    async def submit_raydium_swap(
        self,
        owner_address: str,
        in_token: str,
        out_token: str,
        in_amount: float,
        slippage: float = 0,
        compute_limit: int = 0,
        compute_price: int = 0,
        tip: int = 0,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        swap = await self.post_raydium_swap(post_raydium_swap_request=api.PostRaydiumSwapRequest(
            owner_address=owner_address,
            in_token=in_token,
            out_token=out_token,
            in_amount=in_amount,
            slippage=slippage,
            compute_limit=compute_limit,
            compute_price=compute_price,
            tip=tip
        ))

        signed_tx = transaction.sign_tx_message_with_private_key(
            swap.transactions[0], pk
        )

        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )

        return result.signature

    async def submit_raydium_swap_cpmm(
        self,
        owner_address: str,
        in_token: str,
        out_token: str,
        in_amount: float,
        slippage: float = 0,
        compute_limit: int = 0,
        compute_price: int = 0,
        tip: int = 0,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        swap = await self.post_raydium_cpmm_swap(post_raydium_cpmm_swap_request=api.PostRaydiumCpmmSwapRequest(
            owner_address=owner_address,
            in_token=in_token,
            out_token=out_token,
            in_amount=in_amount,
            slippage=slippage,
            compute_limit=compute_limit,
            compute_price=compute_price,
            tip=tip
        ))

        signed_tx = transaction.sign_tx_message_with_private_key(
            swap.transaction, pk
        )

        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )

        return result.signature

    async def submit_raydium_swap_clmm(
        self,
        owner_address: str,
        in_token: str,
        out_token: str,
        in_amount: float,
        slippage: float = 0,
        compute_limit: int = 0,
        compute_price: int = 0,
        tip: int = 0,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        swap = await self.post_raydium_clmm_swap(post_raydium_swap_request=api.PostRaydiumSwapRequest(
            owner_address=owner_address,
            in_token=in_token,
            out_token=out_token,
            in_amount=in_amount,
            slippage=slippage,
            compute_limit=compute_limit,
            compute_price=compute_price,
            tip=tip
        ))

        signed_tx = transaction.sign_tx_message_with_private_key(
            swap.transactions[0], pk
        )

        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )

        return result.signature

    async def submit_jupiter_swap(
        self,
        owner_address: str,
        in_token: str,
        out_token: str,
        in_amount: float,
        slippage: float = 0,
        compute_limit: int = 0,
        compute_price: int = 0,
        tip: int = 0,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        swap = await self.post_jupiter_swap(post_jupiter_swap_request=api.PostJupiterSwapRequest(
            owner_address=owner_address,
            in_token=in_token,
            out_token=out_token,
            in_amount=in_amount,
            slippage=slippage,
            compute_limit=compute_limit,
            compute_price=compute_price,
            tip=tip
        ))

        signed_tx = transaction.sign_tx_message_with_private_key(
            swap.transactions[0], pk
        )

        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )

        return result.signature

    async def submit_pump_fun_swap(
        self,
        owner_address: str,
        bonding_curve_address: str,
        token_address: str,
        token_amount: float,
        sol_threshold: float,
        is_buy: bool,
        compute_limit: int = 0,
        compute_price: int = 0,
        tip: int = 0,
        skip_pre_flight: bool = True,
    ) -> str:
        pk = self.require_private_key()
        swap = await self.post_pump_fun_swap(post_pump_fun_swap_request=api.PostPumpFunSwapRequest(
            user_address=owner_address,
            bonding_curve_address=bonding_curve_address,
            token_address=token_address,
            token_amount=token_amount,
            sol_threshold=sol_threshold,
            is_buy=is_buy,
            compute_limit=compute_limit,
            compute_price=compute_price,
            tip=tip
        ))

        signed_tx = transaction.sign_tx_message_with_private_key_v2(
            swap.transaction, pk
        )

        result = await self.post_submit(
            post_submit_request=api.PostSubmitRequest(
                transaction=signed_tx, skip_pre_flight=skip_pre_flight
            )
        )

        return result.signature
    
    async def submit_snipe(
        self,
        transactions: List[str],
        use_staked_rpcs: bool = False,
        skip_pre_flight: bool = False,
    ) -> List[str]:
            pk = self.require_private_key()
            
            entries = []
            for tx in transactions:
                signed_tx = transaction.sign_tx_message_with_private_key(tx, pk)
                entries.append(
                    api.PostSubmitRequestEntry(
                        transaction=signed_tx,
                        skip_pre_flight=skip_pre_flight
                    )
                )

            result = await self.post_submit_snipe_v2(
                post_submit_snipe_request=api.PostSubmitSnipeRequest(
                    entries=entries,
                    use_staked_rp_cs=use_staked_rpcs
                )
            )
            
            return [
                entry.signature 
                for entry in result.transactions 
                if entry.submitted
            ]

    async def submit_paladin(
        self,
        transaction_message: str,
    ) -> str:
        pk = self.require_private_key()
        signed_tx = transaction.sign_tx_message_with_private_key(
            transaction_message, 
            pk
        )
        
        result = await self.post_submit_paladin(
            post_submit_paladin_request=api.PostSubmitPaladinRequest(
                transaction=api.TransactionMessageV2(
                    content=signed_tx.content
                )
            )
        )
        
        return result.signature


class NotConnectedException(Exception):
    pass
