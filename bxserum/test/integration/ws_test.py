import aiounittest
from bxserum import provider
import public

class TestWS(aiounittest.AsyncTestCase):
    async def ws_test(self):
        async with provider.WsProvider as ws:
            await public.test_orderbook_equivalent_input_formats(self, ws)
            await public.test_orderbook_different_markets(self, ws)
            await public.test_markets(self, ws)