from asyncio.log import logger
import base64
from collections.abc import Callable, Awaitable
from pprint import pprint

from solders.hash import Hash

from bxsolana import provider
from bxsolana_trader_proto import api as proto

import os

from bxsolana.transaction import create_trader_api_tip_tx_signed, load_private_key_from_env

from solders import pubkey as pk # pyre-ignore[21]: module is too hard to find
from solders import instruction as inst # pyre-ignore[21]: module is too hard to find
from solders import transaction as solders_tx  # pyre-ignore[21]: module is too hard to find
from solders.hash import Hash
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.compute_budget import set_compute_unit_price
from solders.transaction import VersionedTransaction
from solders import message as msg # pyre-ignore[21]: module is too hard to find
import base64



class Endpoint:
    func: Callable[[provider.Provider], Awaitable[bool]]
    requires_additional_env_vars: bool

    def __init__(self, func: Callable[[provider.Provider], Awaitable[bool]], requires_additional_env_vars: bool):
        self.func = func
        self.requires_additional_env_vars = requires_additional_env_vars


class EnvironmentVariables:
    private_key: str
    public_key: str
    open_orders_address: str
    payer: str

    def __init__(self, private_key, public_key, open_orders_address, payer):
        self.private_key = private_key
        self.public_key = public_key
        self.open_orders_address = open_orders_address
        self.payer = payer


def initializeEnvironmentVariables() -> EnvironmentVariables:
    if not os.getenv("AUTH_HEADER"):
        logger.critical("Must specify bloXroute authorization header!")
        raise SystemExit("AUTH_HEADER environment variable is required!")

    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        logger.error("PRIVATE_KEY environment variable not set. Cannot run examples requiring transaction submission.")

    public_key = os.getenv("PUBLIC_KEY")
    if not public_key:
        logger.warning("PUBLIC_KEY environment variable not set. Will skip place/cancel/settle examples.")

    open_orders_address = os.getenv("OPEN_ORDERS")
    if not open_orders_address:
        logger.error("OPEN_ORDERS environment variable not set. Requests may be slower.")

    payer = os.getenv("PAYER")
    if not payer:
        if public_key:
            logger.warning("PAYER environment variable not set. Defaulting to PUBLIC_KEY as payer.")
            payer = public_key
        else:
            payer = ""
            logger.error("PAYER and PUBLIC_KEY environment variables are both unset. PAYER cannot be defaulted.")

    return EnvironmentVariables(
        private_key=private_key or "",
        public_key=public_key or "",
        payer=payer,
        open_orders_address=""
    )


UserEnvironment = initializeEnvironmentVariables()

async def get_transaction(p: provider.Provider) -> bool:
    resp = await p.get_transaction(
        proto.GetTransactionRequest(
            signature="2s48MnhH54GfJbRwwiEK7iWKoEh3uNbS2zDEVBPNu7DaCjPXe3bfqo6RuCg9NgHRFDn3L28sMVfEh65xevf4o5W3"))
    pprint(resp)

    return True if resp.slot is not None else False


async def get_recent_blockhash(p: provider.Provider) -> bool:
    resp = await p.get_recent_block_hash_v2(proto.GetRecentBlockHashRequestV2())
    pprint(resp)

    return True if resp.block_hash is not None else False


async def get_recent_blockhash_offset(p: provider.Provider) -> bool:
    resp = await p.get_recent_block_hash_v2(proto.GetRecentBlockHashRequestV2(offset=1))
    pprint(resp)

    return True if resp.block_hash is not None else False


async def get_rate_limit(p: provider.Provider) -> bool:
    resp = await p.get_rate_limit(proto.GetRateLimitRequest())
    pprint(resp)

    return True if resp.limit is not None else False


async def get_account_balance(p: provider.Provider) -> bool:
    if UserEnvironment.public_key != "":
        resp = await p.get_account_balance_v2(
            proto.GetAccountBalanceRequest(owner_address=UserEnvironment.public_key))
        pprint(resp)

    else:
        resp = await p.get_account_balance_v2(
            proto.GetAccountBalanceRequest(owner_address="HxFLKUAmAMLz1jtT3hbvCMELwH5H9tpM2QugP8sKyfhc"))
        pprint(resp)

    return True if resp.tokens is not None else False


async def get_jupiter_quotes(p: provider.Provider) -> bool:
    resp = await p.get_jupiter_quotes(
        proto.GetJupiterQuotesRequest(in_token="So11111111111111111111111111111111111111112",
                                      out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                                      in_amount=0.01,
                                      slippage=5))

    pprint(resp)

    return True if resp.out_token is not None else False


async def get_pump_fun_quotes(p: provider.Provider) -> bool:
    p = provider.http_pump_ny()

    resp = await p.get_pump_fun_quotes(
        proto.GetPumpFunQuotesRequest(quote_type="buy",
                                      bonding_curve_address="Dga6eouREJ4kLHMqWWtccGGPsGebexuBYrcepBVd494q",
                                      mint_address="9QG5NHnfqQCyZ9SKhz7BzfjPseTFWaApmAtBTziXLanY",
                                      amount=0.01, slippage=5))

    pprint(resp)

    return True if resp.out_amount is not None else False

async def get_priority_fee(p: provider.Provider) -> bool:
    resp = await p.get_priority_fee(proto.GetPriorityFeeRequest())
    pprint(resp)

    return True if resp.fee_at_percentile is not None else False


async def get_token_accounts(p: provider.Provider) -> bool:
    resp = await p.get_token_accounts(proto.GetTokenAccountsRequest(owner_address=UserEnvironment.public_key))
    pprint(resp)

    return True if resp.accounts is not None else False


async def get_pump_fun_new_amm_pool_stream(p: provider.Provider) -> bool:
    print("streaming new pump swap amm pools")

    await p.close()

    p = provider.grpc_pump_ny()
    await p.connect()

    async for resp in p.get_pump_fun_new_amm_pool_stream(
        get_pump_fun_new_amm_pool_stream_request=proto.GetPumpFunNewAmmPoolStreamRequest()
    ):
        pprint(resp)
        await p.close()

        return True if resp.pool is not None else False

    return False


async def get_pump_fun_amm_swap_stream(p: provider.Provider) -> bool:
    print("streaming new pump swap amm swaps")

    await p.close()

    p = provider.grpc_pump_ny()
    await p.connect()

    async for resp in p.get_pump_fun_amm_swap_stream(
        get_pump_fun_amm_swap_stream_request=proto.GetPumpFunAmmSwapStreamRequest(
            pools=["4w2cysotX6czaUGmmWg13hDpY4QEMG2CzeKYEQyK9Ama"]
        )
    ):
        pprint(resp)
        await p.close()

        return True if resp.tx_hash is not None else False

    return False


async def get_recent_blockhash_stream(p: provider.Provider) -> bool:
    print("streaming recent block hashes...")
    async for resp in p.get_recent_block_hash_stream(
            get_recent_block_hash_request=proto.GetRecentBlockHashRequest(
            )
    ):
        pprint(resp)

        await p.close()
        return True if resp.block_hash is not None else False
    return False

async def get_recent_pump_fun_token() -> proto.GetPumpFunNewTokensStreamResponse:
    print("getting new pump fun token...")
    
    # Don't close the provider inside this function if it's needed elsewhere
    p = provider.grpc_pump_ny()
    await p.connect()
    try:
        request = proto.GetPumpFunNewTokensStreamRequest()
        async for resp in p.get_pump_fun_new_tokens_stream(request):
            return resp
    except Exception as e:
        print(f"Error getting pump fun token: {e}")
        raise
    finally:
        await p.close()
    
    # If we didn't get any responses
    return None

async def get_block_stream(p: provider.Provider) -> bool:
    print("streaming pool reserves...")
    async for resp in p.get_block_stream(get_block_stream_request=proto.GetBlockStreamRequest()):
        pprint(resp)

        await p.close()
        return True if resp.block is not None else False
    return False


async def get_priority_fee_stream(p: provider.Provider) -> bool:
    print("streaming priority fee updates...")
    async for resp in p.get_priority_fee_stream(
            get_priority_fee_request=proto.GetPriorityFeeRequest()
    ):
        pprint(resp)
        await p.close()

        return True if resp.fee_at_percentile is not None else False
    return False


async def get_bundle_tip_stream(p: provider.Provider) -> bool:
    print("streaming bundle tip updates...")
    async for resp in p.get_bundle_tip_stream(
            get_bundle_tip_request=proto.GetBundleTipRequest()
    ):
        pprint(resp)
        await p.close()

        return True if resp.timestamp is not None else False
    return False

async def get_priority_fee_by_program_stream(p: provider.Provider) -> bool:
    print("streaming priority fee by program updates...")
    async for resp in p.get_priority_fee_by_program_stream(
            get_priority_fee_by_program_request=proto.GetPriorityFeeByProgramRequest(
                programs=[
                    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
                    "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK",
                    "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C"
                ]
            )
    ):
        pprint(resp)
        await p.close()

        return True if resp.data is not None else False
    return False

async def call_jupiter_trade_swap(p: provider.Provider) -> bool:
    print("calling post submit jupiter trade swap...")

    response = await p.submit_jupiter_swap(
        owner_address=UserEnvironment.public_key,
        in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        out_token="So11111111111111111111111111111111111111112",
        slippage=0.5,
        in_amount=0.01,
        compute_price=160000,
        compute_limit=200000,
        tip=1100000,
    )

    print("signature for jupiter swap tx", response)

    return True if response != "" else False

async def call_pump_fun_trade_swap(p: provider.Provider) -> bool:
    print("calling pump fun trade swap...")

    await p.close()

    p = provider.http_pump_ny()
    await p.connect()

    new_token = await get_recent_pump_fun_token()

    response = await p.submit_pump_fun_swap(
        owner_address=UserEnvironment.public_key,
        bonding_curve_address=new_token.bonding_curve,
        token_address=new_token.mint,
        creator=new_token.creator,
        token_amount=10,
        sol_threshold=0.0001,
        is_buy=True,
        compute_price=160000,
        compute_limit=200000,
        tip=1100000,
    )

    await p.close()

    print("signature for pump fun swap tx", response)

    return True if response != "" else False

async def get_pump_fun_amm_quotes(p: provider.Provider) -> bool:
    print("calling get_pump_fun_amm_quotes...")

    await p.close()

    p = provider.http_pump_ny()
    await p.connect()

    response = await p.get_pump_fun_amm_quotes(
        get_pump_fun_amm_quotes_request=proto.GetPumpFunAmmQuotesRequest(
            in_token="So11111111111111111111111111111111111111112",
            in_amount=10,
            out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            pool="Gf7sXMoP8iRw4iiXmJ1nq4vxcRycbGXy5RL8a8LnTd3v",
            slippage=0.9
        )
    )

    await p.close()

    print("get_pump_fun_amm_quotes response", response)

    return True if response != "" else False

async def post_pump_fun_amm_swap(p: provider.Provider) -> bool:
    print("calling post_pump_fun_amm_swap...")

    await p.close()

    p = provider.http_pump_ny()
    await p.connect()

    response = await p.post_pump_fun_amm_swap(
        post_pump_fun_amm_swap_request=proto.PostPumpFunAmmSwapRequest(
            owner_address=UserEnvironment.public_key,
            in_token="So11111111111111111111111111111111111111112",
            in_amount=10,
            out_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            pool="Gf7sXMoP8iRw4iiXmJ1nq4vxcRycbGXy5RL8a8LnTd3v",
            slippage=0.9,
            compute_limit=130000,
            compute_price=100000,
            tip=1000000,
        )
    )

    await p.close()

    print("post_pump_fun_amm_swap response", response)

    return True if response != "" else False

async def create_personal_tx_and_submit(p: provider.Provider) -> bool:
    print("creating own transaction and submitting to trader api... ")

    resp = await p.get_recent_block_hash_v2(proto.GetRecentBlockHashRequestV2())

    tx = create_trader_api_tip_tx_signed(
        tip_amount=1100000,
        sender_address=load_private_key_from_env(),
        blockhash=Hash.from_string(resp.block_hash)
    )

    response = await p.post_submit(proto.PostSubmitRequest(
        transaction=tx,
        skip_pre_flight=True)
    )


    print("signature for custom user tx", response)

    return True if response != "" else False


async def call_submit_snipe(p: provider.Provider) -> bool:
    resp = await p.get_recent_block_hash_v2(proto.GetRecentBlockHashRequestV2())
    blockhash = Hash.from_string(resp.block_hash)
    
    fee_payer = Keypair()
    small_tip = 100_000
    staked_tip_threshold = 1_000_000
    tip_wallet = Pubkey.from_string("HWEoBxYs7ssKuudEjzjmpfJVX7Dvi7wescFsVx2L5yoY")
    jito_tip_wallet = Pubkey.from_string("96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5")

    # First transaction: transfer to both jito and bloxroute
    tx1_instructions = [
        transfer(TransferParams(
            from_pubkey=fee_payer.pubkey(),
            to_pubkey=jito_tip_wallet,
            lamports=small_tip
        )),
        transfer(TransferParams(
            from_pubkey=fee_payer.pubkey(),
            to_pubkey=tip_wallet, 
            lamports=small_tip
        ))
    ]

    tx1_message = MessageV0.try_compile(
        payer=fee_payer.pubkey(),
        instructions=tx1_instructions,
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash
    )
    tx1 = VersionedTransaction(tx1_message, [fee_payer])
    signature1 = fee_payer.sign_message(msg.to_bytes_versioned(tx1.message))
    tx1 = VersionedTransaction.populate(tx1.message, [signature1])

    # Second transaction: staked transfer to bloxroute
    tx2_instructions = [
        transfer(TransferParams(
            from_pubkey=fee_payer.pubkey(),
            to_pubkey=tip_wallet,
            lamports=staked_tip_threshold
        ))
    ]
    
    tx2_message = MessageV0.try_compile(
        payer=fee_payer.pubkey(),
        instructions=tx2_instructions,
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash
    )
    tx2 = VersionedTransaction(tx2_message, [fee_payer])
    signature2 = fee_payer.sign_message(msg.to_bytes_versioned(tx2.message))
    tx2 = VersionedTransaction.populate(tx2.message, [signature2])

    transactions = [
        proto.TransactionMessage(
            content=base64.b64encode(bytes(tx1)).decode(),
            is_cleanup=False
        ),
        proto.TransactionMessage(
            content=base64.b64encode(bytes(tx2)).decode(),
            is_cleanup=False
        )
    ]

    result = await p.submit_snipe(transactions, use_staked_rpcs=True)
    print("Snipe Signatures:", result)
    return len(result) > 0

async def call_place_order_bundle_paladin(p: provider.Provider) -> bool:
    print("Starting place order with bundle using Paladin...")
    
    # Get recent blockhash
    resp = await p.get_recent_block_hash_v2(proto.GetRecentBlockHashRequestV2())
    blockhash = Hash.from_string(resp.block_hash)
    
    # Load private key from environment
    private_key = load_private_key_from_env()
    
    # Create instructions
    # 1. Set compute unit price instruction
    compute_budget_ix = set_compute_unit_price(
        200000000
    )
    
    # 2. Transfer instruction
    transfer_ix = transfer(TransferParams(
        from_pubkey=private_key.pubkey(),
        to_pubkey=Pubkey.from_string("HWEoBxYs7ssKuudEjzjmpfJVX7Dvi7wescFsVx2L5yoY"),
        lamports=10000000
    ))
    
    # Compile message
    tx_message = MessageV0.try_compile(
        payer=private_key.pubkey(),
        instructions=[compute_budget_ix, transfer_ix],
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash
    )
    
    # Create transaction
    tx = VersionedTransaction(tx_message, [private_key])
    signature = private_key.sign_message(msg.to_bytes_versioned(tx.message))
    tx = VersionedTransaction.populate(tx.message, [signature])
    
    # Encode transaction
    tx_base64 = base64.b64encode(bytes(tx)).decode()
    
    # Submit transaction using paladin
    try:
        signature = await p.submit_paladin(
            signed_tx=tx_base64,
            revert_protection=True
        )
        
        print(f"Submitted order to trader API with signature: {signature}")
        return True
    except Exception as e:
        print(f"Failed to sign and submit order: {e}")
        return False
