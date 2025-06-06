from enum import Enum
from typing import Tuple

# Warning messages
WARNING_TLS_SLOWDOWN = "Performance Notice: Secure (TLS) endpoints may introduce latency due to handshake overhead. For optimal trading speed, consider using non-secure endpoints when appropriate."

# Base hostnames
_HOSTS = {
    "ny": "ny.solana.dex.blxrbdn.com",
    "uk": "uk.solana.dex.blxrbdn.com", 
    "la": "la.solana.dex.blxrbdn.com",
    "frankfurt": "germany.solana.dex.blxrbdn.com",
    "amsterdam": "amsterdam.solana.dex.blxrbdn.com",
    "tokyo": "tokyo.solana.dex.blxrbdn.com",
    "pump_ny": "pump-ny.solana.dex.blxrbdn.com",
    "pump_uk": "pump-uk.solana.dex.blxrbdn.com",
    "testnet": "solana.dex.bxrtest.com",
    "devnet": "solana-trader-api-nlb-6b0f765f2fc759e1.elb.us-east-1.amazonaws.com",
}

class Region(Enum):
    NY = "NY"
    UK = "UK"
    LA = "LA"
    AMS = "AMS"
    TOKYO = "TOKYO"
    FRANKFURT = "FRANKFURT"

class ConnectionType(Enum):
    GRPC = "gRPC"
    HTTP = "HTTP" 
    WS = "WS"

# Port constants
GRPC_PORT_INSECURE = 80
GRPC_PORT_SECURE = 443
TESTNET_GRPC_PORT = 443
DEVNET_GRPC_PORT = 80
LOCAL_GRPC_PORT = 9000

def _build_endpoint(host: str, connection: ConnectionType, secure: bool) -> str:
    """Build endpoint URL based on connection type and security."""
    if connection == ConnectionType.HTTP:
        prefix = "https" if secure else "http"
        return f"{prefix}://{host}"
    elif connection == ConnectionType.WS:
        prefix = "wss" if secure else "ws"
        return f"{prefix}://{host}/ws"
    else:
        raise ValueError(f"Unsupported connection type for URL building: {connection}")

def get_endpoint(region: Region, connection: ConnectionType, secure: bool = True, pump: bool = False) -> str | Tuple[str, int]:
    """
    Get endpoint for specified region, connection type, and TLS settings.
    
    Args:
        region: Target region
        connection: Connection type (HTTP, WS, or GRPC)
        secure: Whether to use secure connection
        pump: Whether to use pump-specific endpoints
        
    Returns:
        For HTTP/WS: URL string
        For GRPC: Tuple of (host, port)
    """
    # Handle pump endpoints
    if pump:
        if region == Region.NY:
            host = _HOSTS["pump_ny"]
        elif region == Region.UK:
            host = _HOSTS["pump_uk"]
        else:
            raise ValueError(f"Pump endpoints not supported for region {region.value}")
    else:
        # Map regions to hosts
        region_map = {
            Region.NY: _HOSTS["ny"],
            Region.UK: _HOSTS["uk"],
            Region.LA: _HOSTS["la"],
            Region.AMS: _HOSTS["amsterdam"],
            Region.TOKYO: _HOSTS["tokyo"],
            Region.FRANKFURT: _HOSTS["frankfurt"],
        }
        
        if region not in region_map:
            raise ValueError(f"Unknown region: {region.value}")
        
        host = region_map[region]
    
    # Return based on connection type
    if connection == ConnectionType.GRPC:
        port = GRPC_PORT_SECURE if secure else GRPC_PORT_INSECURE
        return host, port
    else:
        return _build_endpoint(host, connection, secure)

# Convenience functions for backward compatibility
def get_grpc_endpoint(region: Region, secure: bool = False, pump: bool = False) -> Tuple[str, int]:
    """Get GRPC endpoint as (host, port) tuple."""
    return get_endpoint(region, ConnectionType.GRPC, secure, pump)

def get_http_endpoint(region: Region, secure: bool = False, pump: bool = False) -> str:
    """Get HTTP endpoint URL."""
    return get_endpoint(region, ConnectionType.HTTP, secure, pump)

def get_ws_endpoint(region: Region, secure: bool = False, pump: bool = False) -> str:
    """Get WebSocket endpoint URL."""
    return get_endpoint(region, ConnectionType.WS, secure, pump)

# Special environment endpoints
def get_testnet_endpoint(connection: ConnectionType, secure: bool = False) -> str | Tuple[str, int]:
    """Get testnet endpoint (always secure)."""
    host = _HOSTS["testnet"]
    if connection == ConnectionType.GRPC:
        return host, TESTNET_GRPC_PORT
    else:
        return _build_endpoint(host, connection, secure=secure)

def get_devnet_endpoint(connection: ConnectionType, secure: bool = False) -> str | Tuple[str, int]:
    """Get devnet endpoint (always insecure)."""
    host = _HOSTS["devnet"]
    if connection == ConnectionType.GRPC:
        return host, DEVNET_GRPC_PORT
    else:
        return _build_endpoint(host, connection, secure=secure)

def get_local_endpoint(connection: ConnectionType) -> str | Tuple[str, int]:
    """Get local development endpoint."""
    if connection == ConnectionType.GRPC:
        return "127.0.0.1", LOCAL_GRPC_PORT
    elif connection == ConnectionType.HTTP:
        return "http://127.0.0.1:9000"
    elif connection == ConnectionType.WS:
        return "ws://127.0.0.1:9000/ws"