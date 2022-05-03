import asyncio
from async_timeout import timeout
import bxserum
from unittest import TestCase
from typing import AsyncGenerator

stream_expect_entries = 3
stream_expect_timeout = 60

async def test_stream(t: TestCase, stream: AsyncGenerator):
    try:
        for i in range(stream_expect_entries):
            async with timeout(stream_expect_timeout):
                await stream.__anext__()
    except asyncio.TimeoutError:
        t.fail("no value found in " + str(stream_expect_timeout) + " seconds")


async def test_orderbook_stream(t: TestCase, p: bxserum.Api):
    stream = p.get_orderbook_stream(market="SOL/USDT")
    await test_stream(t, stream)