from . import provider
from . import examples

Provider = provider.Provider


async def trader_api(connection_provider: Provider) -> Provider:
    await connection_provider.connect()
    return connection_provider


__all__ = [
    "examples",
    "Provider",
    "trader_api",
]
