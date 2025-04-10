import aiounittest

from . import private
from bxsolana import provider


class TestHTTP(aiounittest.AsyncTestCase):
    
    async def test_http_private(self):
        async with provider.http() as http:
            await private.test_submit_cancel_order(self, http)
