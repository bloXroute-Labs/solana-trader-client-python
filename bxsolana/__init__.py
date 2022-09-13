from bxsolana import provider

Provider = provider.Provider


async def trader_api(connection_provider: Provider) -> Provider:
    await connection_provider.connect()
    return connection_provider


_all = ["trader_api", "Provider"]
