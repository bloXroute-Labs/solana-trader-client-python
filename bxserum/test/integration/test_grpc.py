import aiounittest
from bxserum import provider
import public

class TestGRPC(aiounittest.AsyncTestCase):
    async def test_grpc(self):
        async with provider.GrpcProvider() as grpc:
            await public.test_orderbook_equivalent_input_formats(self, grpc)
            await public.test_orderbook_different_markets(self, grpc)
            await public.test_markets(self, grpc)
