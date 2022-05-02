import aiounittest
from bxserum import provider


class TestHTTP(aiounittest.AsyncTestCase):
    async def test_orderbook_equivalent_input_formats(self):
        async with provider.HttpProvider() as http:
            orderbook1 = await http.get_orderbook(market="ETHUSDT")
            self.assertIsNotNone(orderbook1)
            self.assertEqual(orderbook1.market, "ETHUSDT")

            orderbook2 = await http.get_orderbook(market="ETH-USDT")
            self.assertIsNotNone(orderbook2)
            self.assertEqual(orderbook2.market, "ETH-USDT")

            orderbook3 = await http.get_orderbook(market="ETH:USDT")
            self.assertIsNotNone(orderbook3)
            self.assertEqual(orderbook3.market, "ETH:USDT")

            self.assertEqual(orderbook1.asks, orderbook2.asks)
            self.assertEqual(orderbook2.asks, orderbook3.asks)

            self.assertEqual(orderbook1.bids, orderbook2.bids)
            self.assertEqual(orderbook2.bids, orderbook3.bids)

    async def test_orderbook_different_markets(self):
        async with provider.HttpProvider() as http:
            orderbook1 = await http.get_orderbook(market="ETHUSDT")
            self.assertIsNotNone(orderbook1)
            self.assertEqual(orderbook1.market, "ETHUSDT")

            orderbook2 = await http.get_orderbook(market="BTCUSDC")
            self.assertIsNotNone(orderbook2)
            self.assertEqual(orderbook2.market, "BTCUSDC")

            orderbook3 = await http.get_orderbook(market="MSRMUSDC")
            self.assertIsNotNone(orderbook3)
            self.assertEqual(orderbook3.market, "MSRMUSDC")

            orderbook4 = await http.get_orderbook(market="xCOPEUSDC")
            self.assertIsNotNone(orderbook4)
            self.assertEqual(orderbook4.market, "xCOPEUSDC")

    async def test_markets(self):
        async with provider.HttpProvider() as http:
            markets = await http.get_markets()
            self.assertIsNotNone(markets)

            market1 = markets.markets["AAVE/USDT"]
            self.assertIsNotNone(market1)

            market2 = markets.markets["LINK/USDC"]
            self.assertIsNotNone(market2)

            market3 = markets.markets["MSRM/USDC"]
            self.assertIsNotNone(market3)

            market4 = markets.markets["YFI/USDC"]
            self.assertIsNotNone(market4)
