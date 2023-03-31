import asyncio
import unittest
import random

import aiohttp
import jsonrpc
from bxsolana_trader_proto.common import OrderType
from grpclib import GRPCError
from solana import keypair


from bxsolana import provider, proto, transaction


async def test_submit_cancel_order(t: unittest.TestCase, p: provider.Provider):
    private_key = transaction.load_private_key_from_env()
    public_key = str(private_key.public_key)
    open_orders_address = transaction.load_open_orders()

    client_order_id = random.randint(1000000000, 9999999999)

    tx_hash = await p.submit_order(
        public_key,
        public_key,
        "SOLUSDC",
        proto.Side.S_ASK,
        [OrderType.OT_LIMIT],
        0.1,
        10_000,
        open_orders_address,
        client_order_id,
    )
    await verify_tx(t, tx_hash)

    tx_cancel_hash = await p.submit_cancel_by_client_order_i_d(
        client_order_id,
        "9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT",
        public_key,
        open_orders_address,
    )
    await verify_tx(t, tx_cancel_hash)

    try:
        # payer mismatch
        await p.submit_order(
            public_key,
            public_key,
            "SOLUSDC",
            proto.Side.S_BID,
            [OrderType.OT_LIMIT],
            0.1,
            10_000,
        )
        t.fail("unexpectedly received no error from payer mismatch")
    except (GRPCError, provider.HttpError) as e:
        t.assertEqual(
            "invalid payer specified: owner cannot match payer unless"
            " selling SOL",
            e.message,
        )
    except jsonrpc.RpcError as e:
        t.assertEqual(
            "invalid payer specified: owner cannot match payer unless"
            " selling SOL",
            e.data,
        )

    try:
        # quantity too low
        await p.submit_order(
            public_key,
            public_key,
            "SOLUSDC",
            proto.Side.S_ASK,
            [OrderType.OT_LIMIT],
            0.000001,
            10_000,
        )
        t.fail("unexpectedly received no error from quantity too low")
    except (GRPCError, provider.HttpError) as e:
        t.assertEqual(
            "Transaction simulation failed: Error processing Instruction 2: "
            "invalid program argument",
            e.message,
        )
    except jsonrpc.RpcError as e:
        t.assertEqual(
            "Transaction simulation failed: Error processing Instruction 2: "
            "invalid program argument",
            e.data,
        )

    kp = keypair.Keypair()
    try:
        # bad open orders address
        await p.submit_order(
            public_key,
            public_key,
            "SOLUSDC",
            proto.Side.S_ASK,
            [OrderType.OT_LIMIT],
            0.1,
            10_000,
            str(kp.public_key),
        )
        t.fail("unexpectedly received no error from bad open orders address")
    except (GRPCError, provider.HttpError) as e:
        t.assertEqual(
            "Transaction simulation failed: Error processing Instruction 2: "
            "custom program error: 0x10000a4",
            e.message,
        )
    except jsonrpc.RpcError as e:
        t.assertEqual(
            "Transaction simulation failed: Error processing Instruction 2: "
            "custom program error: 0x10000a4",
            e.data,
        )


async def verify_tx(t: unittest.TestCase, tx_hash: str):
    attempts = 0

    while attempts < 5:
        try:
            result_hash = await check_solscan(tx_hash)
            t.assertEqual(tx_hash, result_hash)
            return
        except:  # noqa: E722
            pass

        attempts += 1
        await asyncio.sleep(10)
    t.fail(f"could not find transaction hash in timeout: {tx_hash}")


async def check_solscan(tx_hash: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://public-api.solscan.io/transaction/{tx_hash}"
        ) as resp:
            return (await resp.json())["txHash"]
