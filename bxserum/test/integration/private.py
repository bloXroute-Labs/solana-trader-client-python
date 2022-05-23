import asyncio
import unittest

import aiohttp

from bxserum import provider, transaction, proto

SUBMIT_GOOD_ORDERS = False


async def test_submit_order(t: unittest.TestCase, p: provider.Provider):
    private_key = transaction.load_private_key()
    public_key = private_key.public_key

    if SUBMIT_GOOD_ORDERS:
        tx_hash = await p.submit_order(
            str(public_key),
            str(public_key),
            "SOL/USDC",
            proto.Side.S_ASK,
            [proto.OrderType.OT_LIMIT],
            0.1,
            10_000
        )
        await verify_tx(t, tx_hash)


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
        async with session.get(f"https://public-api.solscan.io/transaction/{tx_hash}") as resp:
            return (await resp.json())["TxHash"]
