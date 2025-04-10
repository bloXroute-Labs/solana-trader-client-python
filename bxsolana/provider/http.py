import os
from typing import Type, AsyncGenerator, Optional, TYPE_CHECKING, List, Any

import aiohttp

from solders import keypair as kp  # pyre-ignore[21]: module is too hard to find

from bxsolana_trader_proto import api as proto
from grpclib.metadata import Deadline
from grpclib.metadata import _MetadataLike as MetadataLike
from .. import transaction
from . import constants
from .base import Provider
from .http_error import map_response
from .package_info import NAME, VERSION

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    # pyre-ignore[21]: module is too hard to find
    from grpclib._protocols import IProtoMessage

    # noinspection PyProtectedMember
    from betterproto import T


class HttpProvider(Provider):
    _endpoint: str # pyre-ignore[11]: annotation
    _endpoint_v2: str # pyre-ignore[11]: annotation
    _session: aiohttp.ClientSession # pyre-ignore[11]: annotation
    _private_key: Optional[kp.Keypair] # pyre-ignore[11]: annotation

    # noinspection PyMissingConstructor
    def __init__(
        self,
        endpoint: str = constants.MAINNET_API_UK_HTTP,
        auth_header: Optional[str] = None,
        private_key: Optional[str] = None,
    ):
        self._endpoint = f'{endpoint}/api/v1'
        self._endpoint_v2 = f'{endpoint}/api/v2'
        if auth_header is None:
            auth_header = os.environ["AUTH_HEADER"]

        self._session = aiohttp.ClientSession()
        self._session.headers["authorization"] = auth_header
        self._session.headers["x-sdk"] = NAME
        self._session.headers["x-sdk-version"] = VERSION

        if private_key is None:
            try:
                self._private_key = transaction.load_private_key_from_env()
            except EnvironmentError:
                self._private_key = None
        else:
            self._private_key = transaction.load_private_key(private_key)

    async def connect(self):
        pass

    def private_key(self) -> Optional[kp.Keypair]:
        return self._private_key

    async def close(self):
        await self._session.close()

    async def get_rate_limit(
        self,
        get_rate_limit_request: proto.GetRateLimitRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRateLimitResponse:

        print(f"{self._endpoint_v2}/rate-limit")

        async with self._session.get(f"{self._endpoint_v2}/rate-limit") as res:
            return await map_response(res, proto.GetRateLimitResponse())

    async def get_transaction(
        self,
        get_transaction_request: proto.GetTransactionRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetTransactionResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/transaction?signature={get_transaction_request.signature}"
        ) as res:
            return await map_response(res, proto.GetTransactionResponse())

    async def get_raydium_pools(
        self,
        get_raydium_pools_request: proto.GetRaydiumPoolsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumPoolsResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/pools"
        ) as res:
            return await map_response(res, proto.GetRaydiumPoolsResponse())

    async def get_raydium_clmm_pools(
        self,
        get_raydium_clmm_pools_request: proto.GetRaydiumClmmPoolsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumClmmPoolsResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/clmm-pools"
            f"?pairOrAddress={get_raydium_clmm_pools_request.pair_or_address}"
        ) as res:
            return await map_response(res, proto.GetRaydiumClmmPoolsResponse())

    async def get_raydium_pool_reserve(
        self,
        get_raydium_pool_reserve_request: proto.GetRaydiumPoolReserveRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumPoolReserveResponse:
        params = "?" + serialize_list(
            "pairsOrAddresses",
            get_raydium_pool_reserve_request.pairs_or_addresses,
        )
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/pool-reserves{params}"
        ) as res:
            return await map_response(
                res, proto.GetRaydiumPoolReserveResponse()
            )

    async def get_raydium_quotes(
        self,
        get_raydium_quotes_request: proto.GetRaydiumQuotesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumQuotesResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/quotes?inToken={get_raydium_quotes_request.in_token}&"
            f"outToken={get_raydium_quotes_request.out_token}&inAmount={get_raydium_quotes_request.in_amount}&"
            f"slippage={get_raydium_quotes_request.slippage}"
        ) as res:
            return await map_response(res, proto.GetRaydiumQuotesResponse())

    async def get_pump_fun_quotes(
        self,
        get_pump_fun_quotes_request: proto.GetPumpFunQuotesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetPumpFunQuotesResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/pumpfun/quotes?quoteType={get_pump_fun_quotes_request.quote_type}&"
            f"amount={get_pump_fun_quotes_request.amount}&"
            f"bondingCurveAddress={get_pump_fun_quotes_request.bonding_curve_address}&"
            f"mintAddress={get_pump_fun_quotes_request.mint_address}&"
            f"slippage={get_pump_fun_quotes_request.slippage}"
        ) as res:
            return await map_response(res, proto.GetPumpFunQuotesResponse())

    async def get_raydium_clmm_quotes(
        self,
        get_raydium_clmm_quotes_request: proto.GetRaydiumClmmQuotesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumClmmQuotesResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/clmm-quotes?inToken={get_raydium_clmm_quotes_request.in_token}&"
            f"outToken={get_raydium_clmm_quotes_request.out_token}&inAmount={get_raydium_clmm_quotes_request.in_amount}&"
            f"slippage={get_raydium_clmm_quotes_request.slippage}"
        ) as res:
            return await map_response(res, proto.GetRaydiumQuotesResponse())

    async def get_raydium_cpmm_quotes(
        self,
        get_raydium_cpmm_quotes_request: proto.GetRaydiumCpmmQuotesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumCpmmQuotesResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/clmm-quotes?inToken={get_raydium_cpmm_quotes_request.in_token}&"
            f"outToken={get_raydium_cpmm_quotes_request.out_token}&inAmount={get_raydium_cpmm_quotes_request.in_amount}&"
            f"slippage={get_raydium_cpmm_quotes_request.slippage}"
        ) as res:
            return await map_response(res, proto.GetRaydiumCpmmQuotesResponse())

    async def get_jupiter_quotes(
        self,
        get_jupiter_quotes_request: proto.GetJupiterQuotesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetJupiterQuotesResponse:
        url = (
            f"{self._endpoint_v2}/jupiter/quotes?inToken={get_jupiter_quotes_request.in_token}&"
            f"outToken={get_jupiter_quotes_request.out_token}&inAmount={get_jupiter_quotes_request.in_amount}&"
            f"slippage={get_jupiter_quotes_request.slippage}"
        )
        async with self._session.get(url) as res:
            return await map_response(res, proto.GetJupiterQuotesResponse())

    async def get_raydium_prices(
        self,
        get_raydium_prices_request: proto.GetRaydiumPricesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRaydiumPricesResponse:
        params = "?" + serialize_list(
            "tokens", get_raydium_prices_request.tokens
        )
        async with self._session.get(
            f"{self._endpoint_v2}/raydium/prices{params}"
        ) as res:
            return await map_response(res, proto.GetRaydiumPricesResponse())

    async def get_jupiter_prices(
        self,
        get_jupiter_prices_request: proto.GetJupiterPricesRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetJupiterPricesResponse:
        params = "?" + serialize_list(
            "tokens", get_jupiter_prices_request.tokens
        )
        async with self._session.get(
            f"{self._endpoint_v2}/jupiter/prices{params}"
        ) as res:
            return await map_response(res, proto.GetJupiterPricesResponse())
        
    async def get_leader_schedule(
        self,
        get_leader_schedule_request: proto.GetLeaderScheduleRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetLeaderScheduleResponse:
        async with self._session.get(
            f"{self._endpoint_v2}/system/leader-schedule?maxSlots={get_leader_schedule_request.max_slots}"
        ) as res:
            return await map_response(res, proto.GetLeaderScheduleResponse())

    async def post_jupiter_swap(
        self,
        post_jupiter_swap_request: proto.PostJupiterSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostJupiterSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/jupiter/swap",
            json=post_jupiter_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostJupiterSwapResponse())

    async def post_raydium_swap(
        self,
        post_raydium_swap_request: proto.PostRaydiumSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostRaydiumSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/raydium/swap",
            json=post_raydium_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostRaydiumSwapResponse())

    async def post_raydium_cpmm_swap(
        self,
        post_raydium_cpmm_swap_request: proto.PostRaydiumCpmmSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostRaydiumCpmmSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/raydium/cpmm-swap",
            json=post_raydium_cpmm_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostRaydiumCpmmSwapResponse())

    async def post_raydium_clmm_swap(
        self,
        post_raydium_swap_request: proto.PostRaydiumSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostRaydiumSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/raydium/clmm-swap",
            json=post_raydium_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostRaydiumSwapResponse())

    async def post_pump_fun_swap(
        self,
        post_pump_fun_swap_request: proto.PostPumpFunSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostPumpFunSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/pumpfun/swap",
            json=post_pump_fun_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostPumpFunSwapResponse())

    async def post_jupiter_route_swap(
        self,
        post_jupiter_route_swap_request: proto.PostJupiterRouteSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostJupiterRouteSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/jupiter/route-swap",
            json=post_jupiter_route_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostJupiterRouteSwapResponse())

    async def post_raydium_route_swap(
        self,
        post_raydium_route_swap_request: proto.PostRaydiumRouteSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostRaydiumRouteSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/raydium/route-swap",
            json=post_raydium_route_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostRaydiumRouteSwapResponse())

    async def post_raydium_clmm_route_swap(
        self,
        post_raydium_route_swap_request: proto.PostRaydiumRouteSwapRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostRaydiumRouteSwapResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/raydium/clmm-route-swap",
            json=post_raydium_route_swap_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostRaydiumRouteSwapResponse())

    async def get_token_accounts(
        self,
        get_token_accounts_request: proto.GetTokenAccountsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetTokenAccountsResponse:
        async with self._session.get(
            f"{self._endpoint}/account/token-accounts?ownerAddress={get_token_accounts_request.owner_address}"
        ) as res:
            return await map_response(res, proto.GetTokenAccountsResponse())

    async def get_pools(
        self,
        get_pools_request: proto.GetPoolsRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetPoolsResponse:
        params = "?" + serialize_projects(get_pools_request.projects)

        async with self._session.get(
            f"{self._endpoint}/market/pools{params}"
        ) as res:
            return await map_response(res, proto.GetPoolsResponse())

    async def get_recent_block_hash(
        self,
        get_recent_block_hash_request: proto.GetRecentBlockHashRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRecentBlockHashResponse:
        async with self._session.get(
            f"{self._endpoint}/system/blockhash"
        ) as res:
            return await map_response(res, proto.GetRecentBlockHashResponse())

    async def get_recent_block_hash_v2(
        self,
        get_recent_block_hash_request_v2: proto.GetRecentBlockHashRequestV2,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetRecentBlockHashResponseV2:
        async with self._session.get(
            f"{self._endpoint_v2}/system/blockhash?offset={get_recent_block_hash_request_v2.offset}"
        ) as res:
            return await map_response(res, proto.GetRecentBlockHashResponseV2())

    async def get_priority_fee(
        self,
        get_priority_fee_request: proto.GetPriorityFeeRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetPriorityFeeResponse:
        percentile = getattr(get_priority_fee_request, "percentile", None)
        url = f"{self._endpoint_v2}/system/priority-fee?project={get_priority_fee_request.project.name}"
        if percentile is not None:
            url += f"&percentile={percentile}"

        async with self._session.get(url) as res:
            return await map_response(res, proto.GetPriorityFeeResponse())

    async def get_priority_fee_by_program(
        self,
        get_priority_fee_by_program_request: proto.GetPriorityFeeByProgramRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.GetPriorityFeeResponse:
        url_params = "&programs=".join(get_priority_fee_by_program_request.programs)
        url = f"{self._endpoint_v2}/system/priority-fee-by-program?programs={url_params}"

        async with self._session.get(url) as res:
            return await map_response(res, proto.GetPriorityFeeByProgramResponse())

    async def post_submit(
        self,
        post_submit_request: proto.PostSubmitRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSubmitResponse:
        if transaction is None:
            raise ValueError("transaction cannot be omitted")

        post_submit_request_dict = post_submit_request.to_dict()
        if "useStakedRpCs" in post_submit_request_dict:
            post_submit_request_dict["useStakedRPCs"] = (post_submit_request_dict.pop("useStakedRpCs"))

        async with self._session.post(
            f"{self._endpoint}/trade/submit", json=post_submit_request_dict
        ) as res:
            return await map_response(res, proto.PostSubmitResponse())

    async def post_submit_batch(
        self,
        post_submit_batch_request: proto.PostSubmitBatchRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSubmitBatchResponse:
        async with self._session.post(
            f"{self._endpoint}/trade/submit-batch",
            json=post_submit_batch_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostSubmitBatchResponse())

    async def post_submit_v2(
        self,
        post_submit_request: proto.PostSubmitRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSubmitResponse:
        if transaction is None:
            raise ValueError("transaction cannot be omitted")

        async with self._session.post(
            f"{self._endpoint_v2}/submit", json=post_submit_request.to_dict()
        ) as res:
            return await map_response(res, proto.PostSubmitResponse())

    async def post_submit_batch_v2(
        self,
        post_submit_batch_request: proto.PostSubmitBatchRequest,
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> proto.PostSubmitBatchResponse:
        async with self._session.post(
            f"{self._endpoint_v2}/submit-batch",
            json=post_submit_batch_request.to_dict(),
        ) as res:
            return await map_response(res, proto.PostSubmitBatchResponse())

    async def post_submit_snipe_v2(
        self,
        post_submit_snipe_request: "PostSubmitSnipeRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
    ) -> proto.PostSubmitResponse:
        request_dict = post_submit_snipe_request.to_dict()

        if "useStakedRpCs" in request_dict:
            request_dict["useStakedRPCs"] = request_dict.pop("useStakedRpCs")

        async with self._session.post(
            f"{self._endpoint_v2}/submit-snipe",
            json=request_dict,
        ) as res:
            return await map_response(res, proto.PostSubmitSnipeResponse())

    async def _unary_stream(
        self,
        route: str,
        # pyre-ignore[11]: type is too hard to find
        request: "IProtoMessage",
        response_type: Type["T"],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> AsyncGenerator["T", None]:
        raise NotImplementedError(
            "streaming is not implemented in HTTP provider"
        )

        # useless line to turn function into a generator
        yield response_type()


def serialize_list(key: str, values: List[Any]) -> str:
    parts = []
    for i, v in enumerate(values):
        parts.append(f"{key}={v}")
        if i != len(values) - 1:
            parts.append("&")
    return "".join(parts)


def serialize_projects(projects: List[proto.Project]) -> str:
    return serialize_list("projects", [project.name for project in projects])


def http(region: Optional[constants.Region] = None) -> Provider:
    # default to UK if no region specified
    if region is None or region == constants.Region.UK:
        endpoint = constants.MAINNET_API_UK_HTTP
    elif region == constants.Region.NY:
        endpoint = constants.MAINNET_API_NY_HTTP
    else:
        raise ValueError(f"Unsupported region: {region}")

    return HttpProvider(endpoint=endpoint)

def http_testnet() -> Provider:
    return HttpProvider(endpoint=constants.TESTNET_API_HTTP)


def http_devnet() -> Provider:
    return HttpProvider(endpoint=constants.DEVNET_API_HTTP)


def http_pump_ny() -> Provider:
    return HttpProvider(endpoint=constants.MAINNET_API_PUMP_NY_HTTP)


def http_local() -> Provider:
    return HttpProvider(endpoint=constants.LOCAL_API_HTTP)
