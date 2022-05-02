import aiounittest
from bxserum import provider
class TestWS(aiounittest.AsyncTestCase):
    async def test_orderbook_equivalent_input_formats(self):
        async with provider.WsProvider() as ws:
            orderbook1 = await ws.get_orderbook(market="ETH/USDT")
            self.assertIsNotNone(orderbook1)
            self.assertEqual(orderbook1.market, "ETH/USDT")

            orderbook2 = await ws.get_orderbook(market="ETHUSDT")
            self.assertIsNotNone(orderbook2)
            self.assertEqual(orderbook2.market, "ETHUSDT")

            orderbook3 = await ws.get_orderbook(market="ETH-USDT")
            self.assertIsNotNone(orderbook3)
            self.assertEqual(orderbook3.market, "ETH-USDT")

            orderbook4 = await ws.get_orderbook(market="ETH:USDT")
            self.assertIsNotNone(orderbook4)
            self.assertEqual(orderbook4.market, "ETH:USDT")

            self.assertEqual(orderbook1.asks, orderbook2.asks)
            self.assertEqual(orderbook2.asks, orderbook3.asks)
            self.assertEqual(orderbook3.asks, orderbook4.asks)

            self.assertEqual(orderbook1.bids, orderbook2.bids)
            self.assertEqual(orderbook2.bids, orderbook3.bids)
            self.assertEqual(orderbook3.bids, orderbook4.bids)

    async def test_orderbook_different_markets(self):
        async with provider.WsProvider() as ws:
            orderbook1 = await ws.get_orderbook(market="ETH/USDT")
            self.assertIsNotNone(orderbook1)
            self.assertEqual(orderbook1.market, "ETH/USDT")

            orderbook2 = await ws.get_orderbook(market="BTC/USDC")
            self.assertIsNotNone(orderbook2)
            self.assertEqual(orderbook2.market, "BTC/USDC")

            orderbook3 = await ws.get_orderbook(market="MSRM/USDC")
            self.assertIsNotNone(orderbook3)
            self.assertEqual(orderbook3.market, "MSRM/USDC")

            orderbook4 = await ws.get_orderbook(market="xCOPE/USDC")
            self.assertIsNotNone(orderbook4)
            self.assertEqual(orderbook4.market, "xCOPE/USDC")

    async def test_markets(self):
        async with provider.WsProvider() as ws:
            markets = await ws.get_markets()
            self.assertIsNotNone(markets)

            market1 = markets.markets["AAVE/USDT"]
            self.assertIsNotNone(market1)

            market2 = markets.markets["LINK/USDC"]
            self.assertIsNotNone(market2)

            market3 = markets.markets["MSRM/USDC"]
            self.assertIsNotNone(market3)

            market4 = markets.markets["YFI/USDC"]
            self.assertIsNotNone(market4)
