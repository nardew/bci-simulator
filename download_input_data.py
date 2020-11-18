import os
from collections import defaultdict
import asyncio
import datetime
import json
import time

from pycoingecko import CoinGeckoAPI
from cryptoxlib.CryptoXLib import CryptoXLib

# optionally choose the starting coin for the download. Use None if all coins are to be downloaded
STARTING_COIN = None

# start and end date for the download
START_DT = datetime.datetime(2015, 1, 1)
END_DT = datetime.datetime(2020, 1, 1)


async def run():
    cl = CryptoXLib.create_binance_client(os.environ['BINANCEAPIKEY'], os.environ['BINANCESECKEY'])

    coins = set()

    # download a list of coins supported by binance, the coins will be used as an input for a download from coin gecko
    exchange_info = (await cl.get_exchange_info())['response']
    for symbol in exchange_info['symbols']:
        coins.add(symbol['baseAsset'].upper())

    print(f"Number of coins: {len(coins)}")
    print(f"Coins: {sorted(coins)}")

    cg = CoinGeckoAPI()

    # maps symbol to coin gecko id
    coin_ids = {}
    for coin in cg.get_coins_list():
        if coin['symbol'].upper() in coins:
            # filter major margin coins, stable coins and exchange coins
            if '3x-' not in coin['id'] and \
                    'USDC' not in coin['symbol'].upper() and \
                    'USDS' not in coin['symbol'].upper() and \
                    'USDT' not in coin['symbol'].upper() and \
                    'TUSD' not in coin['symbol'].upper() and \
                    'BGBP' not in coin['symbol'].upper() and \
                    'BUSD' not in coin['symbol'].upper() and \
                    'PAX' not in coin['symbol'].upper() and \
                    'BNB' not in coin['symbol'].upper():
                coin_ids[coin['symbol'].upper()] = coin['id']

    # output is of format {'YYYY-MM-DD': {'coin': {'price': ..., 'cap': ..., 'volume': ...}, ...}
    output = defaultdict(defaultdict)

    try:
        for coin in sorted(coin_ids.keys()):
            coin_id = coin_ids[coin]
            if STARTING_COIN is None or coin >= STARTING_COIN:
                print(f"Downloading {coin} ({coin_id})")

                # attempt to download the data max. 3 times (e.g. because of failures due to too many requests)
                for i in range(0, 3):
                    try:
                        data = cg.get_coin_market_chart_range_by_id(coin_id, 'usd', START_DT.timestamp(), END_DT.timestamp())
                        break
                    except Exception as e:
                        if i == 2:
                            raise e
                        else:
                            print(e)
                            print(f"Retrying after 30sec")
                            time.sleep(30)

                for (price, cap, volume) in reversed(list(zip(data['prices'], data['market_caps'], data['total_volumes']))):
                    date = datetime.datetime.fromtimestamp(price[0] / 1000).strftime("%Y-%m-%d")
                    if coin not in output[date]:
                        output[date][coin] = {}
                    output[date][coin]['price'] = price[1]
                    output[date][coin]['cap'] = cap[1]
                    output[date][coin]['volume'] = volume[1]
    except Exception as e:
        print(e)

    # dump output into a file
    output_file_name = "data.json" if STARTING_COIN is None else f"{STARTING_COIN}.json"
    with open(output_file_name, 'w') as file:
        file.write(json.dumps(output))

    await cl.close()

if __name__ == "__main__":
    asyncio.run(run())