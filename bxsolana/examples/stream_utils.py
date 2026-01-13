from bxsolana_trader_proto import api as proto
from .. import provider


async def do_stream(
    api: provider.Provider, pump: provider.Provider, run_slow: bool = False
):
    item_count = 0
    print("streaming pump fun new tokens...")
    async for response in pump.get_pump_fun_new_tokens_stream(
        get_pump_fun_new_tokens_stream_request=proto.GetPumpFunNewTokensStreamRequest()
    ):
        print(response.to_json())
        async for sresponse in pump.get_pump_fun_swaps_stream(
            get_pump_fun_swaps_stream_request=proto.GetPumpFunSwapsStreamRequest(
                tokens=[response.mint]
            )
        ):
            print(sresponse.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

        item_count += 1
        if item_count == 1:
            item_count = 0
            break

    if run_slow:
        print("streaming priority fee updates...")
        async for response in api.get_priority_fee_stream(
            get_priority_fee_request=proto.GetPriorityFeeRequest()
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming bundle tip updates...")
        async for response in api.get_bundle_tip_stream(
            get_bundle_tip_request=proto.GetBundleTipRequest()
        ):
            print(response.to_json())
            item_count += 1
            if item_count == 1:
                item_count = 0
                break

    if run_slow:
        print("streaming new pump swap amm pools")
        async for response in api.get_pump_fun_new_amm_pool_stream(
            get_pump_fun_new_amm_pool_stream_request=proto.GetPumpFunNewAmmPoolStreamRequest()
        ):
            print(response.to_json())
            item_count+=1 
            if item_count == 1:
                item_count = 0
                break

