from bxserum import proto, provider


def serum(connection_provider: provider.Provider) -> proto.ApiStub:
    return provider.ApiWrapper(connection_provider)
