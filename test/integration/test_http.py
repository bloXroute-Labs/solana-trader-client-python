import aiounittest

from . import private, public
from bxsolana import provider


class TestHTTP(aiounittest.AsyncTestCase):
    async def test_http(self):
        async with provider.http() as http:
            await public.test_orderbook_equivalent_input_formats(self, http)
            await public.test_orderbook_different_markets(self, http)
            await public.test_markets(self, http)

    async def test_http_private(self):
        async with provider.http() as http:
            await private.test_submit_cancel_order(self, http)
