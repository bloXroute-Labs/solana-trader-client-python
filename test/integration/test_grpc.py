import unittest
import asyncio
from bxsolana import provider
from bxsolana_trader_proto import api as proto

class TestGRPC(unittest.TestCase):
    def test_pump_fun_amm_swap_stream(self):
        asyncio.run(self._test_impl())
        
    async def _test_impl(self):
        p = provider.grpc_pump_ny()
        await p.connect()
        request = proto.GetPumpFunAmmSwapStreamRequest(
            pools=["6WwcmiRJFPDNdFmtgVQ8eY1zxMzLKGLrYuUtRy4iZmye"]
        )
        
        try:
            # Get first response only
            async for resp in p.get_pump_fun_amm_swap_stream(request):
                print(resp)
                break
        finally:
            await p.close()