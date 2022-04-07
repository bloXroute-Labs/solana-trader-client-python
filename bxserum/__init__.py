from bxserum import proto, provider

Api = proto.ApiStub


async def serum(connection_provider: provider.Provider) -> Api:
    await connection_provider.connect()
    return connection_provider
