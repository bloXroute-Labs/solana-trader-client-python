import asyncio
from async_timeout import timeout
import bxserum
from unittest import TestCase
from typing import AsyncGenerator

stream_expect_entries = 2
stream_expect_timeout = 60

async def test_stream(t: TestCase, stream: AsyncGenerator):
    counter = 0
    try:
        for i in range(stream_expect_entries):
            async with timeout(stream_expect_timeout):
                await stream.__anext__()
                counter += 1
    except asyncio.TimeoutError:
        t.fail(f"{counter} values found with timeout of {stream_expect_timeout} seconds")

async def test_orderbook_stream(t: TestCase, p: bxserum.Api):
    stream = p.get_orderbook_stream(market="SOL/USDC")
    await test_stream(t, stream)