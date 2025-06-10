import unittest
import asyncio
import sys
import os
# Use local changes when testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from bxsolana import provider
from bxsolana_trader_proto import api as proto

class TestGRPC(unittest.TestCase):
    def test_get_recent_blockhash(self):
        asyncio.run(self._test_impl())
        
    async def _test_impl(self):
        p = provider.http()
        await p.connect()  # Add this
        try:
            request = proto.GetRecentBlockHashRequest()
            response = await p.get_recent_block_hash(request)
            print(response)
        finally:
            await p.close()