import asyncio
import unittest

import aiohttp
from grpclib import GRPCError
from solana import keypair

from bxserum import provider, transaction, proto
from bxserum.provider.http_error import HttpError
from bxserum.provider.wsrpc_error import RpcError

SUBMIT_GOOD_ORDERS = False


async def test_submit_order(t: unittest.TestCase, p: provider.Provider):
    private_key = transaction.load_private_key()
    public_key = str(private_key.public_key)

    if SUBMIT_GOOD_ORDERS:
        tx_hash = await p.submit_order(
            public_key,
            public_key,
            "SOLUSDC",
            proto.Side.S_ASK,
            [proto.OrderType.OT_LIMIT],
            0.1,
            10_000,
        )
        await verify_tx(t, tx_hash)

    try:
        # payer mismatch
        await p.submit_order(
            public_key,
            public_key,
            "SOLUSDC",
            proto.Side.S_BID,
            [proto.OrderType.OT_LIMIT],
            0.1,
            10_000,
        )
        t.fail("unexpectedly received no error from payer mismatch")
    except (GRPCError, HttpError) as e:
        t.assertEqual(
            "invalid payer specified: owner cannot match payer unless selling SOL",
            e.message,
        )
    except RpcError as e:
        t.assertEqual(
            "invalid payer specified: owner cannot match payer unless selling SOL",
            e.data,
        )


    try:
        # quantity too low
        await p.submit_order(
            public_key,
            public_key,
            "SOLUSDC",
            proto.Side.S_ASK,
            [proto.OrderType.OT_LIMIT],
            0.000001,
            10_000,
        )
        t.fail("unexpectedly received no error from quantity too low")
    except (GRPCError, HttpError) as e:
        t.assertEqual(
            "Transaction simulation failed: Error processing Instruction 2: "
            "invalid program argument",
            e.message,
        )
    except RpcError as e:
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
            [proto.OrderType.OT_LIMIT],
            0.1,
            10_000,
            str(kp.public_key)
        )
        t.fail("unexpectedly received no error from bad open orders address")
    except (GRPCError, HttpError) as e:
        t.assertEqual(
            "Transaction simulation failed: Error processing Instruction 2: "
            "custom program error: 0x10000a4",
            e.message,
        )
    except RpcError as e:
        t.assertEqual(
            "Transaction simulation failed: Error processing Instruction 2: "
            "custom program error: 0x10000a4",
            e.data,
        )


async def verify_tx(t: unittest.TestCase, tx_hash: str):
    attempts = 0
    while attempts < 3:
        try:
            result_hash = await check_solscan(tx_hash)
            t.assertEqual(tx_hash, result_hash)
            return
        except:
            pass

        attempts += 1
        await asyncio.sleep(5)
    t.fail("could not find transaction hash in timeout")


async def check_solscan(tx_hash: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://public-api.solscan.io/transaction/{tx_hash}"
        ) as resp:
            return (await resp.json())["TxHash"]
