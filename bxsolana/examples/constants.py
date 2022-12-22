# sample keys to run integration/regression tests with
# maintained by bloxroute team
import json

PUBLIC_KEY = "5ggt7wtjap91P3SPrFfi3QNuXRCn9D9oXcsNeRQH51q3"
USDC_WALLET = "8w1igsiZfsWnMTJSKkSvDQYYCZyf6aXMihuXEYpxcZVD"
OPEN_ORDERS = "4JCZomAb4eKcJQ9fqoi2JPT1TzjbhJEk8V8MmFKUQfnV"
MARKET = "SOLUSDC"
ORDER_ID = ""

try:
    with open("test_state.json") as f:
        cfg = json.load(f)
        PUBLIC_KEY = cfg["publicKey"]
        OPEN_ORDERS = cfg["openOrders"]
        USDC_WALLET = cfg["usdcWallet"]
        MARKET = cfg["market"]
        ORDER_ID = cfg["expectedOrderId"]
except Exception:
    # ignore
    pass
