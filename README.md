# Solana Trader Python Client

Provides a Python SDK for bloXroute's Solana Trader API.

## Installation

```
$ pip install bxsolana-trader
```

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
$ cd solana-trader-client-python
$ pip install -r requirements.txt
```

Run tests:

```
$

```

Regenerate protobuf files:

```
$ make proto
```

Linting:
```
$ make lint
```
