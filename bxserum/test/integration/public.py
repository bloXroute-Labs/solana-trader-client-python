from unittest import TestCase
from bxserum import provider

async def test_orderbook_equivalent_input_formats(t: TestCase, p: provider.Provider):
    orderbook1 = await p.get_orderbook(market="ETHUSDT")
    t.assertIsNotNone(orderbook1)
    t.assertEqual(orderbook1.market, "ETHUSDT")

    orderbook2 = await p.get_orderbook(market="ETH-USDT")
    t.assertIsNotNone(orderbook2)
    t.assertEqual(orderbook2.market, "ETH-USDT")

    orderbook3 = await p.get_orderbook(market="ETH:USDT")
    t.assertIsNotNone(orderbook3)
    t.assertEqual(orderbook3.market, "ETH:USDT")

    t.assertEqual(orderbook1.asks, orderbook2.asks)
    t.assertEqual(orderbook2.asks, orderbook3.asks)

    t.assertEqual(orderbook1.bids, orderbook2.bids)
    t.assertEqual(orderbook2.bids, orderbook3.bids)

    if type(p) != provider.HttpProvider:
        orderbook4 = await p.get_orderbook(market="ETH/USDT")
        t.assertIsNotNone(orderbook4)
        t.assertEqual(orderbook4.market, "ETH/USDT")

        t.assertEqual(orderbook3.asks, orderbook4.asks)
        t.assertEqual(orderbook3.bids, orderbook4.bids)

async def test_orderbook_different_markets(t: TestCase, p: provider.Provider):
    orderbook1 = await p.get_orderbook(market="ETHUSDT")
    t.assertIsNotNone(orderbook1)
    t.assertEqual(orderbook1.market, "ETHUSDT")

    orderbook2 = await p.get_orderbook(market="BTCUSDC")
    t.assertIsNotNone(orderbook2)
    t.assertEqual(orderbook2.market, "BTCUSDC")

    orderbook3 = await p.get_orderbook(market="MSRMUSDC")
    t.assertIsNotNone(orderbook3)
    t.assertEqual(orderbook3.market, "MSRMUSDC")

    orderbook4 = await p.get_orderbook(market="xCOPEUSDC")
    t.assertIsNotNone(orderbook4)
    t.assertEqual(orderbook4.market, "xCOPEUSDC")

async def test_markets(t: TestCase, p: provider.Provider):
    markets = await p.get_markets()
    t.assertIsNotNone(markets)

    market1 = markets.markets["ETH/USDT"]
    t.assertIsNotNone(market1)

    market2 = markets.markets["BTC/USDC"]
    t.assertIsNotNone(market2)

    market3 = markets.markets["MSRM/USDC"]
    t.assertIsNotNone(market3)

    market4 = markets.markets["xCOPE/USDC"]
    t.assertIsNotNone(market4)

