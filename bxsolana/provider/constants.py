_mainnet_virginia = "virginia.solana.dex.blxrbdn.com"
_mainnet_ny = "ny.solana.dex.blxrbdn.com"
_mainnet_frankfurt = "frankfurt.solana.dex.blxrbdn.com"
_mainnet_uk = "uk.solana.dex.blxrbdn.com"
_testnet = "serum-nlb-5a2c3912804344a3.elb.us-east-1.amazonaws.com"
_devnet = "solana-trader-api-nlb-6b0f765f2fc759e1.elb.us-east-1.amazonaws.com"


def http_endpoint(base: str, secure: bool) -> str:
    prefix = "http"
    if secure:
        prefix = "https"
    return f"{prefix}://{base}"


def ws_endpoint(base: str, secure: bool) -> str:
    prefix = "ws"
    if secure:
        prefix = "wss"
    return f"{prefix}://{base}/ws"


MAINNET_API_VIRGINIA_HTTP = http_endpoint(_mainnet_virginia, True)
MAINNET_API_VIRGINIA_WS = ws_endpoint(_mainnet_virginia, True)
MAINNET_API_VIRGINIA_GRPC_HOST = _mainnet_virginia

MAINNET_API_NY_HTTP = http_endpoint(_mainnet_ny, True)
MAINNET_API_NY_WS = ws_endpoint(_mainnet_ny, True)
MAINNET_API_NY_GRPC_HOST = _mainnet_ny

MAINNET_API_FRANKFURT_HTTP = http_endpoint(_mainnet_frankfurt, True)
MAINNET_API_FRANKFURT_WS = ws_endpoint(_mainnet_frankfurt, True)
MAINNET_API_FRANKFURT_GRPC_HOST = _mainnet_frankfurt

MAINNET_API_UK_HTTP = http_endpoint(_mainnet_uk, True)
MAINNET_API_UK_WS = ws_endpoint(_mainnet_uk, True)
MAINNET_API_UK_GRPC_HOST = _mainnet_uk

MAINNET_API_GRPC_PORT = 443

TESTNET_API_HTTP = http_endpoint(_testnet, False)
TESTNET_API_WS = ws_endpoint(_testnet, False)
TESTNET_API_GRPC_HOST = _testnet
TESTNET_API_GRPC_PORT = 80

DEVNET_API_HTTP = http_endpoint(_devnet, False)
DEVNET_API_WS = ws_endpoint(_devnet, False)
DEVNET_API_GRPC_HOST = _devnet
DEVNET_API_GRPC_PORT = 80

LOCAL_API_HTTP = "http://127.0.0.1:9000"
LOCAL_API_WS = "ws://127.0.0.1:9000/ws"
LOCAL_API_GRPC_HOST = "127.0.0.1"
LOCAL_API_GRPC_PORT = 9000
