from bxserum import proto, provider

Api = proto.ApiStub


def serum(connection_provider: provider.Provider) -> Api:
    return connection_provider
