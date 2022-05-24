import aiounittest
from bxserum import provider
import public, stream
from bxserum.test.integration import private


class TestGRPC(aiounittest.AsyncTestCase):
    async def test_grpc_public(self):
        async with provider.GrpcProvider() as grpc:
            await public.test_orderbook_equivalent_input_formats(self, grpc)
            await public.test_orderbook_different_markets(self, grpc)
            await public.test_markets(self, grpc)

    async def test_grpc_private(self):
        async with provider.GrpcProvider() as grpc:
            await private.test_submit_order(self, grpc)

    async def test_grpc_stream(self):
        async with provider.GrpcProvider() as grpc:
            await stream.test_orderbook_stream(self, grpc)
