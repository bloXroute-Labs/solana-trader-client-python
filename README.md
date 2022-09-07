# Serum Python Client

Provides a Python SDK for bloXroute's Serum API.

## Installation

```
$ pip install bxserum
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

Context manager:

```python
from bxserum import provider

async with provider.http() as api:
    print(await api.get_orderbook(market="ETHUSDT"))
    
async with provider.ws() as api:
    async for update in api.get_orderbooks_stream(market="ETHUSDT"):
        print(update)
```

Manual:
```python
import bxserum

from bxserum import provider

p = provider.grpc()
api = await bxserum.serum(p)

try:
    await api.get_orderbook(market="ETHUSDT")
finally:
    await p.close()
```

Refer to the `examples/` for more info.

## Development

bloXroute Serum API's interfaces are primarily powered by protobuf, so you will 
need to install it for your system: https://grpc.io/docs/protoc-installation/

Clone project and install dependencies:

```
$ git clone https://github.com/bloXroute-Labs/serum-client-python.git
$ cd serum-client-python
$ pip install -r requirements.txt
```

Run tests:

```
$ make test
```

Regenerate protobuf files:

```
$ make proto
```

Linting:
```
$ make lint
```