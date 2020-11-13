# Bitpanda Crypto Index Simulator

Bitpanda Crypto Index (BCI) is an index product offered by the Austrian crypto broker bitpanda. The index consits of preselected crypto assets based on their actual market capitalization and gets recalculated (rebalanced) monthly to reflect shifts in the market. For full description read the [prospectus](https://cdn.bitpanda.com/media/bci/Prospectus_Index_English.pdf).

This package serves to simulate BCI calculation, determine its composition and perform monthly rebalancing based on the historical input data in order to calculate yield and compare it with the returns resulting from holding the original assets without any rebalancing. This may help decide whether investing in the index is profitable or at least help compare performance with different parameters.

The package tries to simulate BCI rules as much as possible but this cannot be achieved 100% due to certain steps being not explicitly described in the prospectus and bitpanda reserving rights to potentially adjust the rules fully at their sole discretion. Nevertheless, outcome of the simulation still provides valuable insight into mechanics of the index and its evolution over time.

This simulator is highly configurable but it comes with readymade configuration scripts for `BCI5` and `BCI10` indices (see `bci5.sh` and `bci10.sh`).

Calculation is performed based on the historical data provided in JSON format. The repository already contains a sample input file `input_data.json` which contains prices, market capitalizations and volumes of all cryptocurrencies since 01/01/2015 up to 01/11/2020 as published by `CoinGecko`.

To summarize the results, given current and past cryptomarket conditions investing into crypto indices <ins>at the moment</ins> is questionable. Unlike standard assets, crypto currencies are extremely correlated which defeats diversification. Furthermore, fat tail distribution implies that a few leading currencies drive performance of the index all the time. Based on several executions with various parameters you are often better off distributing initial funds into a few top currencies and sticking to them. Also, rebalancing fees are not negligible. More in the section with results. The index is advantageous in case of sudden uncorrelated crash of one of the top performers. If this is what you are trying to protect from, then index is the right thing for you.

Disclaimer: I am by no means affiliated with bitpanda (though I have been their customer for a couple of years) and this project was developed for personal purposes. 

### Results

As already indicated, BCI5 and BCI10's performance depends on the parameters and timeframe used. While it performed well when bought prior to the 2017 bull run, it underperformes when entered later. There are several factors responsible for this, mainly strong correlation between BTC and other leading currencies and dilution of the few top performing coins due to rebalancing despite their price outperforming other assets.
In the following paragraphs I provide performance of indices executed with different parameters and comparison with a diverse portfolio without rebalancing. Each simulation starts with $1000 and applies 2% fee. All values are shown without fees.  

| Index type | Start date | End date | Baseline closing value | Index closing value | Rebalancing fees |
| --- | --- | --- | --- | --- | --- |
| BCI5 | 01/01/2015 | 03/11/2020 | $22,733.50 | $60,169.04 | $4,975.04 |
| BCI5 | 01/01/2016 | 03/11/2020 | $68,984.27 | $78,541.85 | $6,468.85 |
| BCI5 | 01/01/2017 | 03/11/2020 | $27,187.41 | $31,187.39 | $2,538.08 |
| BCI5 | 01/01/2018 | 03/11/2020 | $496.83 | $400.19 | $19.55 |
| BCI5 | 01/01/2019 | 03/11/2020 | $2,411.43 | $2,215.78 | $51.35 |
| BCI5 | 01/01/2020 | 03/11/2020 | $2,019.78 | $1,971.94 | $24.00 |
| BCI10 | 01/01/2015 | 03/11/2020 | $23,195.13 | $47,634.00 | $4,464.40 |
| BCI10 | 01/01/2016 | 03/11/2020 | $69,289.64 | $64,954.50 | $6,061.99 |
| BCI10 | 01/01/2017 | 03/11/2020 | $24,496.33 | $27,106.29 | $2,496.05 |
| BCI10 | 01/01/2018 | 03/11/2020 | $451.55 | $352.14 | $18.47 |
| BCI10 | 01/01/2019 | 03/11/2020 | $2,292.90 | $2,111.58 | $47.83 |
| BCI10 | 01/01/2020 | 03/11/2020 | $1,963.38 | $1,936.60 | $27.07 |

![BCI5](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index5_2015-01-01_2020-11-03.svg)
![BCI5](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index5_2016-01-01_2020-11-03.svg)
![BCI5](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index5_2017-01-01_2020-11-03.svg)
![BCI5](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index5_2018-01-01_2020-11-03.svg)
![BCI5](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index5_2019-01-01_2020-11-03.svg)
![BCI5](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index5_2020-01-01_2020-11-03.svg)
![BCI10](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index10_2015-01-01_2020-11-03.svg)
![BCI10](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index10_2016-01-01_2020-11-03.svg)
![BCI10](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index10_2017-01-01_2020-11-03.svg)
![BCI10](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index10_2018-01-01_2020-11-03.svg)
![BCI10](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index10_2019-01-01_2020-11-03.svg)
![BCI10](https://raw.githubusercontent.com/nardew/bci-simulator/master/images/index10_2020-01-01_2020-11-03.svg)

### Example

I will demonstrate `BCI5` simulation by executing `bci5.sh` for a period of two months with a single rebalancing and explain the output. Numbers are rounded for sake of readibility.

```bash
bci-simulator$ ./bci5.sh 
Bitpanda Crypto Index Simulator

Simulation period: 2020-10-01 - 2020-11-01

Initializing portfolio for $1000.0... // <= first the initial composition of index is calculated based on the available funds
	Top 5 assets: // <= returns top 5 cryptocurrencies according to their current capitalization
		('BTC', {'price': 10770.8813, 'cap': 196617081790.51, 'volume': 18558607662.68, 'volume_avg': 618620255.42})
		('ETH', {'price': 359.5989, 'cap': 39782583382.89, 'volume': 8037484324.98, 'volume_avg': 267916144.16})
		('XRP', {'price': 0.2413, 'cap': 10899063751.06, 'volume': 1349173492.01, 'volume_avg': 44972449.73})
		('BCH', {'price': 227.4442, 'cap': 4214806111.92, 'volume': 1951827124.33, 'volume_avg': 65060904.14})
		('DOT', {'price': 4.3471, 'cap': 3998481295.79, 'volume': 131549097.16, 'volume_avg': 4384969.90})
	Percentage allocation according to capitalization: // <= calculate weight for each currency based on their capitalization
		['BTC', 0.76]
		['ETH', 0.15]
		['XRP', 0.04]
		['BCH', 0.01]
		['DOT', 0.01]
	Capped percentage allocation: // <= cap allocation at 35% per currency
		['BTC', 0.35]
		['ETH', 0.35]
		['XRP', 0.17]
		['BCH', 0.06]
		['DOT', 0.06]
Portfolio allocation: {'BTC': 0.032495019554024604, 'ETH': 0.9733064186554691, 'XRP': 708.8565070308487, 'BCH': 0.29087729992403616, 'DOT': 14.437528683013289}

Rebalancing 2020-11-01 // <= rebalancing occurs (there is only one in this example)
	Primary filtering: // <= first filter out coins from the index if average running volume is less than $600k
		BTC: value $: 10,421,794,299,498.24 (average volume: 756373349.31, price: 13778.6376)
		ETH: value $: 115,873,709,651.78 (average volume: 300311869.12, price: 385.8445)
		XRP: value $: 10,692,339.96 (average volume: 44616541.87, price: 0.2396)
		BCH: value $: 17,892,998,542.04 (average volume: 68397980.41, price: 261.6012)
		DOT: value $: 12,692,380.64 (average volume: 3037895.39, price: 4.1780)
		Preserved coins: ['BTC', 'ETH', 'XRP', 'BCH', 'DOT']
	Secondary filtering: // <= perform another filtering for rest of the coins and limit $1M
		LINK: value $: 349,656,122.95 (average volume: 31148194.07, price: 11.2255)
		LTC: value $: 3,659,559,609.50 (average volume: 65691484.73, price: 55.7082)
		ADA: value $: 1,138,191.11 (average volume: 12255799.57, price: 0.0928)
		EOS: value $: 117,559,867.06 (average volume: 46529621.35, price: 2.5265)
		XMR: value $: 1,439,447,767.04 (average volume: 11403045.21, price: 126.2336)
	Candidate list: ['BTC', 'ETH', 'XRP', 'BCH', 'DOT', 'LINK', 'LTC', 'ADA', 'EOS', 'XMR']
	Sorted candidate list: // <= resulting list of candidates and their capitalizations
		BTC:	254,260,250,527.50
		ETH:	44,687,833,549.98
		XRP:	10,856,481,131.01
		BCH:	4,864,602,893.16
		LINK:	4,386,318,369.52
		DOT:	3,874,741,303.68
		LTC:	3,645,413,637.96
		ADA:	2,891,746,978.33
		EOS:	2,392,706,148.82
		XMR:	2,247,877,179.83
	Index composition: ['BTC', 'ETH', 'XRP', 'BCH', 'DOT'] // <= final set of currencies being part of the new index
	Percentage allocation according to capitalization:
		['BTC', 0.79]
		['ETH', 0.14]
		['XRP', 0.03]
		['BCH', 0.01]
		['DOT', 0.01]
	Capped percentage allocation:
		['BTC', 0.35]
		['ETH', 0.35]
		['XRP', 0.16]
		['BCH', 0.07]
		['DOT', 0.05]
	New portfolio allocation: {'BTC': 0.02869301922003787, 'ETH': 1.0246371882920944, 'XRP': 783.4015168786901, 'BCH': 0.3215731090962748, 'DOT': 16.03779352929636}
	Portfolio value: 1,129.57
	Portfolio updates: {'BTC': -0.003802000333986734, 'ETH': 0.051330769636625306, 'XRP': 74.54500984784147, 'BCH': 0.03069580917223863, 'DOT': 1.6002648462830695} // <= rebalancing BUY/SELL transactions
	Fee: 2.09 USD
	Original portfolio value: 1,129.57 // <= portfolio value for holding the original index without rebalancing (in case of a single rebalancing the values are naturally the same)

Overall fee: 2.09
```

### Implemented BCI rules

To verify the correct methodology was used to simulate `BCI` indices, hereunder the implemented rebalancing rules are outlined. In particular, `BCI5` is used for illustration.

- put all currencies from the current index with average daily traded value (volume*price) >= $600,000 over past 30 days into the list of index candidates 
- put remaining currencies ordered by market capitalization with average daily traded value >= $1,000,000 over past 30 days into the list of index candidates
- put top three currencies from the candidate list into the final index
- put additional two currencies from the candidate list into the final index such that currencies from the existing index ranked up to the 7th place take priority
- normalize weights according to the market capitalization
- cap allocation to 35% and renormalize (the step can be performed several times)

### Parameter description

If you want to try your own simulation with custom parameters, below description of configurable arguments may come in handy.

| Parameter | Description |
| --- | --- |
| `--index` | Size of the index (e.g. 5 for BCI5, 10 for BCI10). |
| `--rebalancing` | Rebalancing period in days (e.g. 30 for index to get rebalanced every 30 days). If set to 0, then index will be rebalanced on the first day of every month. |
| `--fee` | Transaction fees applicable to rebalanced amounts. |
| `--max-allocation` | Maximum percentage allocation of an asset in the index (e.g. 0.35, i.e. 35%, for BCI5).
| `--volume-period` | Number of days used to calculate running average daily volume. 30 days by default.
| `--primary-volume-filter` | Minimal USD amount (running average volume * price) used to filter out currencies from the existing index when building a new one, e.g. 600000 for BCI5. If overall traded amount of currency from the existing index is less than this limit, it is not proposed for inclusion in the next index. |
| `--secondary-volume-filter` | Same as `--primary-volume-filter` but for currencies not being part of the current index, e.g. 1000000 for BCI5. |
| `--candidates` | Number of top performing currencies considered for the selection into the index (after passing all filtering rules), e.g. 10 for BCI5 .|
| `--primary-candidates` | Number of top performing currencies from the candidate list which are immediately included in the index, e.g. 3 for BCI5. |
| `--secondary-candidates` | Maximal position in the sorted candidate list which gives priority to currencies from the current index for inclusion in the next one, e.g. 7 for BCI5. |
| `--funds` | Initial funds to start with. |
| `--input-file` | Path to a file with input historical data. |
| `--start-date` | Starting date of the simulation. If not provided, the first date from the input data is used. |
| `--end-date` | Ending date of the simulation. If not provided, the last date from the input data is used. |
| `--graph` | Plot a graph at the end of simulation. |

### Support

If you like the package and you feel like you want to support its further development, then it will be of great help and most appreciated if you:
- file bugs, proposals, pull requests, ...
- spread the word
- donate an arbitrary tip
  * `BTC`: `3GJPT6H6WeuTWR2KwDSEN5qyJq95LEErzf`
  * `ETH`: `0xC7d8673Ee1B01f6F10e40aA416a1b0A746eaBe68`
