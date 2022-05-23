import asyncio
import unittest

import aiohttp
from grpclib import GRPCError

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
        t.fail("unexpectedly recieved no error from payer mismatch")
    except (GRPCError, HttpError, RpcError) as e:
        t.assertEqual("invalid payer specified: owner cannot match payer unless selling SOL", e.message)


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
