import aiounittest
from bxserum import provider
import public
from bxserum.test.integration import private


class TestHTTP(aiounittest.AsyncTestCase):
    async def test_http(self):
        async with provider.HttpProvider() as http:
            await public.test_orderbook_equivalent_input_formats(self, http)
            await public.test_orderbook_different_markets(self, http)
            await public.test_markets(self, http)

    async def test_http_private(self):
        async with provider.HttpProvider("127.0.0.1", 9000) as http:
            await private.test_submit_order(self, http)

