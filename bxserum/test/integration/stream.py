from unittest import TestCase
from bxserum import provider

async def test_orderbook_stream(t: TestCase, p: provider.Provider):
    counter = 0
    market_name = "SOLUSDC"
    async for orderbook in p.get_orderbook_stream(market=market_name):
        t.assertIsNotNone(orderbook)
        t.assertEqual(orderbook.orderbook.market, market_name)

        counter += 1
        if counter == 3:
            return