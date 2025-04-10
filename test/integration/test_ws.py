import aiounittest

from . import private, stream
from bxsolana import provider


class TestWS(aiounittest.AsyncTestCase):

    async def test_ws_private(self):
        async with provider.ws() as ws:
            await private.test_submit_cancel_order(self, ws)

    async def test_ws_stream(self):
        async with provider.ws() as ws:
            await stream.test_orderbook_stream(self, ws)
