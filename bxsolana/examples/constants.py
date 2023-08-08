# sample keys to run integration/regression tests with
# maintained by bloxroute team
import json

SIDE_BID = "bid"
SIDE_ASK = "ask"
TYPE_LIMIT = "limit"
TYPE_IOC = "ioc"
TYPE_POST_ONLY = "postonly"

PUBLIC_KEY = "BgJ8uyf9yhLJaUVESRrqffzwVyQgRi9YvWmpEFaH14kw"
USDC_WALLET = "6QRBKhLeJQNpPqRUz1L1nwARJ1YGsH3QpmVapn5PeWky"
OPEN_ORDERS = "FpLJoV6WkBoAq7VRNWhfFCua64UZobfqyQG1z8ceTaz2"
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
