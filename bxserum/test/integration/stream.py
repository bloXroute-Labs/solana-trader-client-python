import asyncio
import async_timeout
import bxserum
import unittest
import typing

stream_expect_entries = 2
stream_expect_timeout = 60

async def test_stream(t: unittest.TestCase, stream: typing.AsyncGenerator):
    counter = 0
    try:
        for i in range(stream_expect_entries):
            async with async_timeout.timeout(stream_expect_timeout):
                await stream.__anext__()
                counter += 1
    except asyncio.TimeoutError:
        t.fail(f"{counter}/{stream_expect_entries} values found with timeout of {stream_expect_timeout} seconds")

# Works if the market gets updated when running the test
async def test_orderbook_stream(t: unittest.TestCase, p: bxserum.Api):
    stream = p.get_orderbook_stream(market="SOL/USDC")
    await test_stream(t, stream)