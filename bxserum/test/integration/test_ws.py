import aiounittest
from bxserum import provider
import public, stream
from bxserum.test.integration import private


class TestWS(aiounittest.AsyncTestCase):
    async def test_ws(self):
        async with provider.WsProvider() as ws:
            await public.test_orderbook_equivalent_input_formats(self, ws)
            await public.test_orderbook_different_markets(self, ws)
            await public.test_markets(self, ws)

    async def test_ws_private(self):
        async with provider.WsProvider() as ws:
            await private.test_submit_cancel_order(self, ws)

    async def test_ws_stream(self):
        async with provider.WsProvider() as ws:
            await stream.test_orderbook_stream(self, ws)
