import asyncio
import base64
import os

from solana.blockhash import Blockhash

import bxsolana
from bxsolana import provider, transaction
from bxsolana import utils
from bxsolana_trader_proto import api as proto

API_ENV = os.environ.get("API_ENV", "testnet")
if API_ENV not in ["mainnet", "testnet", "local"]:
    raise EnvironmentError(
        f'invalid API_ENV value: {API_ENV} (valid values: "mainnet", "testnet",'
        ' "local)'
    )

# trades stream is infrequent in terms of updates
RUN_SLOW_STREAMS = os.environ.get("RUN_SLOW_STREAMS", "true")
if RUN_SLOW_STREAMS == "false":
    RUN_SLOW_STREAMS = False
else:
    RUN_SLOW_STREAMS = True

RUN_TRADES = os.environ.get("RUN_TRADES", "true")
if RUN_TRADES == "false":
    RUN_TRADES = False
else:
    RUN_TRADES = True

async def main():
    await http()
    await ws()
    await grpc()


async def http():
    # private keys are loaded from environment variable `PRIVATE_KEY` by default
    # alternatively, can specify the key manually in base58 str if loaded from other source
    # p = provider.HttpProvider("127.0.0.1", 9000, private_key="...")

    if API_ENV == "mainnet":
        p = provider.http()
    elif API_ENV == "local":
        p = provider.http_local()
    else:
        p = provider.http_testnet()
    api = await bxsolana.trader_api(p)

    # either `try`/`finally` or `async with` work with each type of provider
    try:
        await utils.do_requests(api, utils.PUBLIC_KEY, utils.OPEN_ORDERS, utils.ORDER_ID, utils.USDC_WALLET, utils.SOL_USDC_MARKET)
        await utils.do_transaction_requests(api, RUN_TRADES, utils.PUBLIC_KEY, utils.PUBLIC_KEY, utils.OPEN_ORDERS, utils.ORDER_ID, utils.USDC_WALLET)
    except Exception as e:
        print(e)
        raise e
    finally:
        await p.close()


async def ws():
    if API_ENV == "mainnet":
        p = provider.ws()
    elif API_ENV == "local":
        p = provider.ws_local()
    else:
        p = provider.ws_testnet()

    async with p as api:
        await utils.do_requests(api, utils.PUBLIC_KEY, utils.OPEN_ORDERS, utils.ORDER_ID, utils.USDC_WALLET, utils.SOL_USDC_MARKET)
        await utils.do_transaction_requests(api, RUN_TRADES, utils.PUBLIC_KEY, utils.PUBLIC_KEY, utils.OPEN_ORDERS, utils.ORDER_ID, utils.USDC_WALLET)
        await utils.do_stream(api, RUN_SLOW_STREAMS)


async def grpc():
    if API_ENV == "mainnet":
        p = provider.grpc()
    elif API_ENV == "local":
        p = provider.grpc_local()
    else:
        p = provider.grpc_testnet()
    api = await bxsolana.trader_api(p)

    try:
        await utils.do_requests(api, utils.PUBLIC_KEY, utils.OPEN_ORDERS, utils.ORDER_ID, utils.USDC_WALLET, utils.SOL_USDC_MARKET)
        await utils.do_transaction_requests(api, RUN_TRADES, utils.PUBLIC_KEY, utils.PUBLIC_KEY, utils.OPEN_ORDERS, utils.ORDER_ID, utils.USDC_WALLET)
        await utils.do_stream(api, RUN_SLOW_STREAMS)
    finally:
        await p.close()

if __name__ == "__main__":
    asyncio.run(main())