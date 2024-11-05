# Solana Trader Python Client

Provides a Python SDK for bloXroute's Solana Trader API.

## Installation

```
$ pip install bxsolana-trader
```

# `solana-trader-client-python` SDK examples

- Historically, examples are run from this directory in the 'bundles', 'provider', and 'transaction' directory, calling a set of functions from the 'bxsolana' package. We have added `sdk.py` to streamline running examples with this SDK, allowing you to run each endpoint/stream individually, on a per provider (WS, GRPC, HTTP) basis. If you would like to modify the examples to change parameters, amounts, etc, feel free to do so in the example functions in the file and rerun.
- If certain examples submit transactions on chain, and you don't see transactions landing, modify parameters of `computeLimit`, `computePrice` and `tip` parameters. These adjust the tip amount to be sent to RPCs as well as priority fees. You can read more about it here: [Trader API Docs](https://docs.bloxroute.com/solana/trader-api-v2)

## How to Run SDK

Set up your Environment Variables:
```
AUTH_HEADER: bloXRoute Auth Header
PRIVATE_KEY: solana signing key to be used for examples
PUBLIC_KEY: solana public key to be used for examples (default `payer` if not specified)
PAYER: payer responsible for transaction fees (optional)
OPEN_ORDERS: openbook open orders address (optional)
```

Once your environment is set run

`python sdk.py`

After this, follow menu to select whatever you want. This should give you a feeling of the services trader-api provides.

## Usage

This library supports HTTP, websockets, and GRPC interfaces. You can use it with
a context manager or handle open/closing yourself.


For any methods involving transaction creation you will need to provide your 
Solana private key. You can provide this via the environment variable 
`PRIVATE_KEY`, or specify it via the provider configuration if you want to load 
it with some other mechanism. See samples for more information. 
As a general note on this: methods named `post_*` (e.g. `post_order`) typically 
do not sign/submit the transaction, only return the raw unsigned transaction. 
This isn't very useful to most users (unless you want to write a signer in a 
different language), and you'll typically want the similarly named `submit_*` 
methods (e.g. `submit_order`). These methods generate, sign, and submit the
transaction all at once.

You will also need your bloXroute authorization header to use these endpoints. By default, this is loaded from the 
`AUTH_HEADER` environment variable.

Context manager:

```python
from bxsolana import provider

async with provider.http() as api:
    print(await api.get_orderbook(market="ETHUSDT"))
    
async with provider.ws() as api:
    async for update in api.get_orderbooks_stream(market="ETHUSDT"):
        print(update)
```

Manual:

```python
import bxsolana

from bxsolana import provider

p = provider.grpc()
api = await bxsolana.trader_api(p)

try:
    await api.get_orderbook(market="ETHUSDT")
finally:
    await p.close()
```

Refer to the `examples/` for more info.

## Development

bloXroute Solana Trader API's interfaces are primarily powered by protobuf, so you will 
need to install it for your system: https://grpc.io/docs/protoc-installation/

Clone project and install dependencies:

```
    $ git clone https://github.com/bloXroute-Labs/solana-trader-client-python.git
```
You can build the **solana-trader-proto-python** directory using these steps:

 - update **setup.cfg**, set the new version of bxsolana-trader-proto, e.g.
```
    bxsolana-trader-proto==0.0.89
```
- run:
```
    $ pip install -r requirements.txt
```

Run tests:
```
    $ make test
```
Linting:
```
    $ make lint
```
