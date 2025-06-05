from enum import Enum

warning_tls_slowdown = "Performance Notice: Secure (TLS) endpoints may introduce latency due to handshake overhead. For optimal trading speed, consider using non-secure endpoints when appropriate."

_mainnet_ny = "ny.solana.dex.blxrbdn.com"
_mainnet_uk = "uk.solana.dex.blxrbdn.com"
_mainnet_la = "la.solana.dex.blxrbdn.com"
_mainnet_frankfurt = "germany.solana.dex.blxrbdn.com"
_mainnet_amsterdam = "amsterdam.solana.dex.blxrbdn.com"
_mainnet_tokyo = "tokyo.solana.dex.blxrbdn.com"
_mainnet_pump_ny = "pump-ny.solana.dex.blxrbdn.com"
_mainnet_pump_uk = "pump-uk.solana.dex.blxrbdn.com"
_testnet = "solana.dex.bxrtest.com"
_devnet = "solana-trader-api-nlb-6b0f765f2fc759e1.elb.us-east-1.amazonaws.com"

def http_endpoint(base: str, secure: bool) -> str:
    prefix = "https" if secure else "http"
    return f"{prefix}://{base}"

def ws_endpoint(base: str, secure: bool) -> str:
    prefix = "wss" if secure else "ws"
    return f"{prefix}://{base}/ws"

# GRPC defined as host and port
MAINNET_API_GRPC_PORT = 80
MAINNET_API_GRPC_PORT_SECURE = 443

MAINNET_API_NY_GRPC_HOST = _mainnet_ny
MAINNET_API_PUMP_NY_GRPC_HOST = _mainnet_pump_ny
MAINNET_API_UK_GRPC_HOST = _mainnet_uk
MAINNET_API_PUMP_UK_GRPC_HOST = _mainnet_uk
MAINNET_API_LA_GRPC_HOST = _mainnet_la
MAINNET_API_AMS_GRPC_HOST = _mainnet_amsterdam
MAINNET_API_FRANKFURT_GRPC_HOST = _mainnet_frankfurt
MAINNET_API_TOKYO_GRPC_HOST = _mainnet_tokyo

_bases = {
    "NY": _mainnet_ny,
    "PUMP_NY": _mainnet_pump_ny,
    "UK": _mainnet_uk,
    "PUMP_UK": _mainnet_pump_uk,
    "LA": _mainnet_la,
    "AMS": _mainnet_amsterdam,
    "TOKYO": _mainnet_tokyo,
    "FRANKFURT": _mainnet_frankfurt,
}

# Create insecure endpoints
for key, base in _bases.items():
    globals()[f"MAINNET_API_{key}_HTTP"] = http_endpoint(base, False)
    globals()[f"MAINNET_API_{key}_WS"] = ws_endpoint(base, False)

# Create secure endpoints
for key, base in _bases.items():
    globals()[f"MAINNET_API_{key}_HTTP_SECURE"] = http_endpoint(base, True)
    globals()[f"MAINNET_API_{key}_WS_SECURE"] = ws_endpoint(base, True)

# Testnet and Devnet
TESTNET_API_HTTP = http_endpoint(_testnet, True)
TESTNET_API_WS = ws_endpoint(_testnet, True)
TESTNET_API_GRPC_HOST = _testnet
TESTNET_API_GRPC_PORT = 443

DEVNET_API_HTTP = http_endpoint(_devnet, False)
DEVNET_API_WS = ws_endpoint(_devnet, False)
DEVNET_API_GRPC_HOST = _devnet
DEVNET_API_GRPC_PORT = 80

LOCAL_API_HTTP = "http://127.0.0.1:9000"
LOCAL_API_WS = "ws://127.0.0.1:9000/ws"
LOCAL_API_GRPC_HOST = "127.0.0.1"
LOCAL_API_GRPC_PORT = 9000