import asyncio
import bxserum
from async_timeout import timeout
from unittest import TestCase

async def test_orderbook_stream(t: TestCase, p: bxserum.Api):
    market_name = "SOL/USDC"
    try:
        async with timeout(30):
            async for orderbook in p.get_orderbook_stream(market=market_name):
                t.assertIsNotNone(orderbook)
                t.assertEqual(orderbook.orderbook.market, market_name)
                return
    except asyncio.TimeoutError:
        t.fail("no value found in 30 seconds")

