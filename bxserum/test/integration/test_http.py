import aiounittest
import bxserum
import public

class TestHTTP(aiounittest.AsyncTestCase):
    async def test_http(self):
        async with bxserum.provider.HttpProvider() as http:
            await public.test_orderbook_equivalent_input_formats(self, http)
            await public.test_orderbook_different_markets(self, http)
            await public.test_markets(self, http)