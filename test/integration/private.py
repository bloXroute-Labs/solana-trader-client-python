import asyncio
import unittest

import aiohttp


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
