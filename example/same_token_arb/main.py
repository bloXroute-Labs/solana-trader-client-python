# 载入资源
import asyncio
from bxsolana.transaction import signing
from bxsolana_trader_proto import api as proto
from bxsolana import provider, examples
from typing import List, Optional
import os


# 初始化DeFi端
pk_data = open("key", "r").read().splitlines()
os.environ["PUBLIC_KEY"] = pk_data[0]
os.environ["PRIVATE_KEY"] = pk_data[1]
os.environ["AUTH_HEADER"] = pk_data[2]
os.environ["API_ENV"] = "mainnet"
public_key = os.getenv("PUBLIC_KEY")
private_key = os.getenv("PRIVATE_KEY")
auth_header = os.getenv("AUTH_HEADER")
pk = signing.load_private_key(private_key)

defi_tokens = [
    {
        "symbol": "JUP",
        "token_mint": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
        "size": 0.6,
    },
    {
        "symbol": "JitoSOL",
        "token_mint": "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn",
        "size": 1,
    },
    {
        "symbol": "JTO",
        "token_mint": "jtojtomepa8beP8AuQc6eXt5FriJwfFMwQx2v2f9mCL",
        "size": 0.6,
    },
    {
        "symbol": "BONK",
        "token_mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
        "size": 70000,
    },
    {
        "symbol": "MNDE",
        "token_mint": "MNDEFzGvMt87ueuHvVU9VcTqsAP5b3fTGPsHuuPA5ey",
        "size": 2.5,
    },
    {
        "symbol": "USDC",
        "token_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "size": 0.75,
    },
]


async def same_token_arb(middle_token, in_amount, slippage, tip):
    async with provider.http() as api:
        unsigned_tx_2 = await api.post_raydium_swap(
            post_raydium_swap_request=proto.PostRaydiumSwapRequest(
                owner_address=public_key,
                in_token="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                in_amount=0.1,
                out_token="So11111111111111111111111111111111111111112",
                slippage=slippage,
                tip=tip,
            )
        )

        unsigned_tx_0 = await api.post_jupiter_swap(
            post_jupiter_swap_request=proto.PostJupiterSwapRequest(
                owner_address=public_key,
                in_token="So11111111111111111111111111111111111111112",
                in_amount=in_amount,
                out_token=middle_token,
                slippage=0.15,
            )
        )

        middle_amount = unsigned_tx_0.out_amount * 0.999
        # print('MiddleToken', middle_token, middle_amount)

        unsigned_tx_1 = await api.post_jupiter_swap(
            post_jupiter_swap_request=proto.PostJupiterSwapRequest(
                owner_address=public_key,
                in_token=middle_token,
                in_amount=middle_amount,
                out_token="So11111111111111111111111111111111111111112",
                slippage=slippage,
            )
        )

        final_amount = unsigned_tx_1.out_amount

        print(
            "wSOL inAmount:",
            in_amount,
            "outAmount:",
            final_amount,
            "| Middle Token:",
            middle_token,
        )

        if final_amount > in_amount * 1.00:
            unsigned_txs = [
                unsigned_tx_0.transactions[0],
                unsigned_tx_1.transactions[0],
                unsigned_tx_2.transactions[0],
            ]

            signed_txs: List[proto.PostSubmitRequestEntry] = []

            for trx in unsigned_txs:
                signed_tx = signing.sign_tx_message_with_private_key(trx, pk)
                signed_txs.append(
                    proto.PostSubmitRequestEntry(
                        transaction=signed_tx,
                        # skip_pre_flight=True
                    )
                )

            res = await api.post_submit_batch(
                post_submit_batch_request=proto.PostSubmitBatchRequest(
                    entries=signed_txs,
                    # submit_strategy=proto.SubmitStrategy.P_SUBMIT_ALL,
                    use_bundle=True,
                )
            )

            print(res.to_json())


print("请输入单次交易金额")
initial_in_amount = float(input())
print("载入成功，开始尝试套利交易")

if __name__ == "__main__":
    while 0 == 0:
        try:
            in_amount = float(initial_in_amount)

            for i in defi_tokens:
                success = asyncio.run(
                    same_token_arb(
                        middle_token=i["token_mint"],
                        in_amount=in_amount,
                        slippage=0.1,
                        tip=50000,
                    )
                )

            # time.sleep(1)
        except KeyboardInterrupt:
            print("Exit!")
            exit()
        except Exception as error:
            print(error)
