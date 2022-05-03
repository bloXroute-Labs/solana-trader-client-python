import aiounittest
import bxserum
import public, stream

class TestWS(aiounittest.AsyncTestCase):
    async def test_ws(self):
        async with bxserum.provider.WsProvider() as ws:
            await public.test_orderbook_equivalent_input_formats(self, ws)
            await public.test_orderbook_different_markets(self, ws)
            await public.test_markets(self, ws)

    async def test_ws_stream(self):
        async with bxserum.provider.WsProvider() as ws:
            await stream.test_orderbook_stream(self, ws)