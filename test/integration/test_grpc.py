import aiounittest

from . import private, stream
from bxsolana import provider


class TestGRPC(aiounittest.AsyncTestCase):

    async def test_grpc_private(self):
        async with provider.grpc() as grpc:
            await private.test_submit_cancel_order(self, grpc)

    async def test_grpc_stream(self):
        async with provider.grpc() as grpc:
            await stream.test_orderbook_stream(self, grpc)
