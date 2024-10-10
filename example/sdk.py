from bxsolana import provider
from colorama import init
from termcolor import colored

import asyncio
import nest_asyncio
import os
import pyfiglet

from example.menu.menu import MenuSelection

from example.samples.helpers import Endpoint, get_markets, get_pools, get_tickers, get_raydium_clmm_pools, \
    get_orderbook, get_raydium_pool_reserves, get_market_depth, get_open_orders, get_transaction, get_recent_blockhash, \
    get_recent_blockhash_offset, get_rate_limit, get_price, get_raydium_pools, get_raydium_prices, get_jupiter_prices, \
    get_unsettled, get_account_balance, get_quotes, get_raydium_quotes, get_raydium_cpmm_quotes, \
    get_raydium_clmm_quotes, get_jupiter_quotes, get_pump_fun_quotes, orderbook_stream, market_depth_stream, \
    get_tickers_stream, get_prices_stream, get_swaps_stream, get_trades_stream, get_new_raydium_pools_stream, \
    get_new_raydium_pools_stream_cpmm, get_recent_blockhash_stream, get_pool_reserve_stream, \
    get_block_stream, get_priority_fee, get_priority_fee_stream, get_bundle_tip_stream, get_token_accounts, \
    call_trade_swap, call_route_trade_swap, call_raydium_trade_swap, call_raydium_cpmm_trade_swap, \
    call_raydium_clmm_trade_swap, call_jupiter_trade_swap, call_pump_fun_trade_swap, create_personal_tx_and_submit

nest_asyncio.apply()
init(autoreset=True)

# ANSI color code for yellow
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_logo():
    # Generate larger ASCII art for the logo
    print(colored("=" * 180))

    logo = pyfiglet.figlet_format("bloxRoute Trader API", font="block", width=250)  # Use 'block' for a bigger font

    # Print the logo in color
    print(colored(logo, 'cyan'))
    print(colored("Welcome to the bloxRoute Trader API!", 'yellow'))
    print(colored("=" * 180))


ExampleEndpoints = {
    "get_markets": Endpoint(func=get_markets, requires_additional_env_vars=False),
    "get_pools": Endpoint(func=get_pools, requires_additional_env_vars=False),
    "get_tickers": Endpoint(func=get_tickers, requires_additional_env_vars=False),
    "get_raydium_clmm_pools": Endpoint(func=get_raydium_clmm_pools, requires_additional_env_vars=False),
    "get_raydium_pool_reserve": Endpoint(func=get_raydium_pool_reserves, requires_additional_env_vars=False),
    "get_raydium_pools": Endpoint(func=get_raydium_pools, requires_additional_env_vars=False),
    "get_orderbook": Endpoint(func=get_orderbook, requires_additional_env_vars=False),
    "get_market_depth": Endpoint(func=get_market_depth, requires_additional_env_vars=False),
    "get_open_orders": Endpoint(func=get_open_orders, requires_additional_env_vars=False),
    "get_transaction": Endpoint(func=get_transaction, requires_additional_env_vars=False),
    "get_recent_blockhash": Endpoint(func=get_recent_blockhash, requires_additional_env_vars=False),
    "get_recent_blockhash_offset": Endpoint(func=get_recent_blockhash_offset, requires_additional_env_vars=False),
    "get_rate_limit": Endpoint(func=get_rate_limit, requires_additional_env_vars=False),
    "get_priority_fee": Endpoint(func=get_priority_fee, requires_additional_env_vars=False),
    "get_token_accounts": Endpoint(func=get_token_accounts, requires_additional_env_vars=True),
    "get_price": Endpoint(func=get_price, requires_additional_env_vars=False),
    "get_raydium_prices": Endpoint(func=get_raydium_prices, requires_additional_env_vars=False),
    "get_jupiter_prices": Endpoint(func=get_jupiter_prices, requires_additional_env_vars=False),
    "get_unsettled": Endpoint(func=get_unsettled, requires_additional_env_vars=False),
    "get_account_balance": Endpoint(func=get_account_balance, requires_additional_env_vars=False),
    "get_quotes": Endpoint(func=get_quotes, requires_additional_env_vars=False),
    "get_raydium_quotes": Endpoint(func=get_raydium_quotes, requires_additional_env_vars=False),
    "get_raydium_cpmm_quotes": Endpoint(func=get_raydium_cpmm_quotes, requires_additional_env_vars=False),
    "get_raydium_clmm_quotes": Endpoint(func=get_raydium_clmm_quotes, requires_additional_env_vars=False),
    "get_jupiter_quotes": Endpoint(func=get_jupiter_quotes, requires_additional_env_vars=False),
    "get_pump_fun_quotes": Endpoint(func=get_pump_fun_quotes, requires_additional_env_vars=False),

    # streaming endpoints
    "orderbook_stream": Endpoint(func=orderbook_stream, requires_additional_env_vars=False),
    "market_depth_stream": Endpoint(func=market_depth_stream, requires_additional_env_vars=False),
    "tickers_stream": Endpoint(func=get_tickers_stream, requires_additional_env_vars=False),
    "prices_stream": Endpoint(func=get_prices_stream, requires_additional_env_vars=False),
    "swaps_stream": Endpoint(func=get_swaps_stream, requires_additional_env_vars=False),
    "trades_stream": Endpoint(func=get_trades_stream, requires_additional_env_vars=False),
    "new_raydium_pools_stream": Endpoint(func=get_new_raydium_pools_stream, requires_additional_env_vars=False),
    "new_raydium_pools_stream_cpmm": Endpoint(func=get_new_raydium_pools_stream_cpmm,
                                              requires_additional_env_vars=False),
    "get_recent_blockhash_stream": Endpoint(func=get_recent_blockhash_stream, requires_additional_env_vars=False),
    "get_pool_reserve": Endpoint(func=get_pool_reserve_stream, requires_additional_env_vars=False),
    "get_block_stream": Endpoint(func=get_block_stream, requires_additional_env_vars=False),
    "get_priority_fee_stream": Endpoint(func=get_priority_fee_stream, requires_additional_env_vars=False),
    "get_bundle_tip_stream": Endpoint(func=get_bundle_tip_stream, requires_additional_env_vars=False),

    # transaction endpoints
    "trade_swap": Endpoint(func=call_trade_swap, requires_additional_env_vars=True),
    "route_trade_swap": Endpoint(func=call_route_trade_swap, requires_additional_env_vars=True),
    "raydium_swap": Endpoint(func=call_raydium_trade_swap, requires_additional_env_vars=True),
    "raydium_cpmm_swap": Endpoint(func=call_raydium_cpmm_trade_swap, requires_additional_env_vars=True),
    "raydium_clmm_swap": Endpoint(func=call_raydium_clmm_trade_swap, requires_additional_env_vars=True),
    "jupiter_swap": Endpoint(func=call_jupiter_trade_swap, requires_additional_env_vars=True),
    "pump_fun_swap": Endpoint(func=call_pump_fun_trade_swap, requires_additional_env_vars=True),
    "create_custom_bloxroute_transfer": Endpoint(func=create_personal_tx_and_submit, requires_additional_env_vars=True),
}


def choose_provider() -> provider.Provider:
    print('Choose protocol for provider: ')
    provider_options = ["http", "grpc", "ws"]
    menu = MenuSelection(provider_options, visible_items=3)
    choice = menu.run()

    print('Choose environment for provider: ')
    provider_options_environment = ["mainnet", "testnet", "local"]

    menu_environment = MenuSelection(provider_options_environment, visible_items=3)
    env = menu_environment.run()

    if env == "mainnet":
        if choice == "http":
            p = provider.http()
        elif choice == "grpc":
            p = provider.grpc()
        else:
            p = provider.ws()

    elif env == "testnet":
        if choice == "http":
            p = provider.http_testnet()
        elif choice == "grpc":
            p = provider.grpc_testnet()
        else:
            p = provider.ws_testnet()

    else:
        if choice == "http":
            p = provider.http_local()
        elif choice == "grpc":
            p = provider.grpc_local()
        else:
            p = provider.ws_local()

    return p


async def sdk_loop():
    menu_options = []

    while True:
        p = choose_provider()

        await p.connect()
        menu_text = list()

        for name in ExampleEndpoints.keys():
            menu_options.append(name)

        menu_options.append("quit")
        menu = MenuSelection(menu_options, visible_items=10)
        choice = menu.run()

        if choice == "quit":
            await p.close()
            break

        for name, endpoint in ExampleEndpoints.items():
            if choice is name:
                example = ExampleEndpoints[name]
                result = await example.func(p)

                prompt = "Success" if result is True else "Failure"

                print("-" * 200)
                print(f'Function {name} executed with result: {prompt}')
                print("-" * 200)

                menu_text.clear()

                await p.close()

                print(f'Press any key to continue...')
                input()



async def main():
    print_logo()

    input()
    os.system('clear')

    await sdk_loop()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Schedule the coroutine with create_task if the loop is already running
            loop.create_task(main())
        else:
            # Run until complete for standard execution environments
            loop.run_until_complete(main())
    except RuntimeError as e:
        print(f"Error: {e}")
