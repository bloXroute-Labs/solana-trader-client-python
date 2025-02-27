from enum import Enum, auto

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

class Region(Enum):
    NY = "NY"
    UK = "UK"

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


MAINNET_API_GRPC_PORT = 443


# TODO: Create Provider level functionality based on region type
MAINNET_API_NY_HTTP = http_endpoint(_mainnet_ny, True)
MAINNET_API_NY_WS = ws_endpoint(_mainnet_ny, True)
MAINNET_API_NY_GRPC_HOST = _mainnet_ny

MAINNET_API_UK_HTTP = http_endpoint(_mainnet_uk, True)
MAINNET_API_UK_WS = ws_endpoint(_mainnet_uk, True)
MAINNET_API_UK_GRPC_HOST = _mainnet_uk

# Pump Only Regions
# The following URLs are used for Trader API instances that support Pump Fun streams (Raydium is disabled)
# Not all documented trader API endpoints are supported
# See documentation: https://docs.bloxroute.com/solana/trader-api/introduction
MAINNET_API_PUMP_NY_HTTP = http_endpoint(_mainnet_pump_ny, True)
MAINNET_API_PUMP_NY_WS = ws_endpoint(_mainnet_pump_ny, True)
MAINNET_API_PUMP_NY_GRPC_HOST = _mainnet_pump_ny

# Submit Only Regions
# Most functionality of Solana Trader API is disabled on the following URLs, however they give coverage to
# tx submissions in many different endpoints in the world
# see documentation: https://docs.bloxroute.com/solana/trader-api/introduction/regions
MAINNET_API_LA_HTTP = http_endpoint(_mainnet_la, True)
MAINNET_API_LA_WS = ws_endpoint(_mainnet_la, True)
MAINNET_API_LA_GRPC_HOST = _mainnet_la

MAINNET_API_AMS_HTTP = http_endpoint(_mainnet_amsterdam, True)
MAINNET_API_AMS_WS = ws_endpoint(_mainnet_amsterdam, True)
MAINNET_API_AMS_GRPC_HOST = _mainnet_amsterdam

MAINNET_API_TOKYO_HTTP = http_endpoint(_mainnet_tokyo, True)
MAINNET_API_TOKYO_WS = ws_endpoint(_mainnet_tokyo, True)
MAINNET_API_TOKYO_GRPC_HOST = _mainnet_tokyo

MAINNET_API_FRANKFURT_HTTP = http_endpoint(_mainnet_frankfurt, True)
MAINNET_API_FRANKFURT_WS = ws_endpoint(_mainnet_frankfurt, True)
MAINNET_API_FRANKFURT_GRPC_HOST = _mainnet_frankfurt

# TESTNET and DEVNET are not stable - Please use with caution
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
