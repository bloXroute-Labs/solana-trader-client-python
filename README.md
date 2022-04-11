# Serum Python Client

Provides a Python SDK for bloXroute's Serum API.

## Installation

```
$ git clone https://github.com/bloXroute-Labs/serum-client-python.git
$ cd serum-client-python
$ pip install -r requirements.txt
```

Installation via `pip` is expected to be supported soon.

## Usage

This library supports HTTP, websockets, and GRPC interfaces. You can use it with
a context manager or handle open/closing yourself.

Context manager:

```python
from bxserum import provider

async with provider.HttpProvider() as api:
    print(await api.get_orderbook(market="ETHUSDT"))
    
async with provider.WsProvider() as api:
    async for update in api.get_orderbook_stream(market="ETHUSDT"):
        print(update)
```

Manual:
```python
import bxserum

from bxserum import provider

p = provider.GrpcProvider()
api = await bxserum.serum(p)

try:
    await api.get_orderbook(market="ETHUSDT")
finally:
    await p.close()
```

Refer to the `examples/` for more info.

