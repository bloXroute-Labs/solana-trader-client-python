import unittest
import asyncio
import sys
import os
# Use local changes when testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from bxsolana import provider
from bxsolana_trader_proto import api as proto

class TestGRPC(unittest.TestCase):
    def test_pump_fun_amm_swap_stream(self):
        asyncio.run(self._test_impl())
        
    async def _test_impl(self):
        p = provider.ws_pump_ny()
        await p.connect()
        request = proto.GetPumpFunAmmSwapStreamRequest(
            pools=["Ef7wUrbarRXHNMMgBs8cstSkzRttnstjMsniaq7zMp6j"]
        )
        
        try:
            # Get first response only
            async for resp in p.get_pump_fun_amm_swap_stream(request):
                print(resp)
                break
        finally:
            await p.close()