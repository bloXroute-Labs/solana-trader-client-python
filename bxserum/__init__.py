from bxserum import proto, provider

Provider = provider.Provider


async def serum(connection_provider: Provider) -> Provider:
    await connection_provider.connect()
    return connection_provider


_all = [
    "serum",
    "Provider"
]
