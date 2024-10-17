# `solana-trader-client-python` SDK examples

- Historically, examples are run from this directory in the 'bundles', 'provider', and 'transaction' directory, calling a set of functions from the 'bxsolana' package. We have added `sdk.py` to streamline running examples with this SDK, allowing you to run each endpoint/stream individually, on a per provider (WS, GRPC, HTTP) basis. If you would like to modify the examples to change parameters, amounts, etc, feel free to do so in the example functions in the file and rerun.
- If certain examples submit transactions on chian, and you don't see transactions landing, modify parameters of `computeLimit`, `computePrice` and `tip` parameters. These adjust the tip amount to be sent to RPCs as well as priority fees. You can read more about it here: [Trader API Docs](https://docs.bloxroute.com/solana/trader-api-v2)

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
