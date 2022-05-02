import aiounittest
from bxserum import provider
import public

class TestHTTP(aiounittest.AsyncTestCase):
    async def http_test(self):
        async with provider.HttpProvider as http:
            await public.test_orderbook_equivalent_input_formats(self, http)
            await public.test_orderbook_different_markets(self, http)
            await public.test_markets(self, http)