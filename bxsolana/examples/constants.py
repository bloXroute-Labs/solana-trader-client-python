# sample keys to run integration/regression tests with
# maintained by bloxroute team
import json

PUBLIC_KEY = "BgJ8uyf9yhLJaUVESRrqffzwVyQgRi9YvWmpEFaH14kw"
USDC_WALLET = "6QRBKhLeJQNpPqRUz1L1nwARJ1YGsH3QpmVapn5PeWky"
MARKET = "SOLUSDC"

try:
    with open("test_state.json") as f:
        cfg = json.load(f)
        PUBLIC_KEY = cfg["publicKey"]
        USDC_WALLET = cfg["usdcWallet"]
except Exception:
    # ignore
    pass
