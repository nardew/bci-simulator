# Bitpanda Crypto Index Simulator

Bitpanda Crypto Index (BCI) is an index product offered by the Austrian crypto broker bitpanda. The index consits of preselected crypto assets based on their actual market capitalization and gets recalculated (rebalanced) monthly to reflect shifts in the market. For full description read the [prospectus](https://cdn.bitpanda.com/media/bci/Prospectus_Index_English.pdf).

This package serves to simulate BCI calculation, determine its composition and perform monthly rebalancing based on the historical input data in order to calculate yield and compare it with the returns resulting from holding the original assets without any rebalancing. This may help decide whether investing in the index is profitable or at least help compare performance with different parameters.

The package tries to simulate BCI rules as much as possible but this cannot be achieved 100% due to certain steps being not explicitly described in the prospectus and bitpanda reserving rights to potentially adjust the rules fully at their sole discretion. Nevertheless, outcome of the simulation still provides valuable insight into mechanics of the index and its evolution over time.

This simulator is highly configurable but it comes with readymade configuration scripts for `BCI5` and `BCI10` indices (see `bci5.sh` and `bci10.sh`).

Calculation is performed based on the historical data provided in JSON format. The repository already contains a sample input file `input_data.json` which contains prices, market capitalizations and volumes of all cryptocurrencies since 01/01/2015 up to 01/11/2020 as published by `CoinGecko`.

To summarize the results, given current and past cryptomarket conditions I do not see a benefit of investing into crypto indices <ins>at the moment</ins>. Unlike standard assets, crypto currencies are extremely correlated which defeats diversification. Furthermore, fat tail distribution implies that a few leading currencies drive performance of the index all the time. Based on several executions with various parameters you are always better off distributing initial funds into a few top currencies and sticking to them. More in the section with results. The index would be advantageous only in case of sudden uncorrelated crash of one of the top performers. If this is what you are trying to protect from, then index is the right thing for you.

Disclaimer: I am by no means affiliated with bitpanda (though I have been their customer for a couple of years) and this project was developed for personal purposes. 

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

### Results

As already mentioned in the introduction, BCI5 and BCI10 underperformed in every single simulation compared to simply holding the original diverse top portfolio. There are several factors responsible for this, mainly strong correlation between BTC and other leading currencies and dilution of the few top performing coins due to rebalancing despite their price outperforming other assets.

In the following paragraphs I provide performance of indices executed with different parameters and comparison with a diverse portfolio without rebalancing. Each simulation starts with $1000 and applies 2% fee. Shown values do not include fees.  

##### BCI5, 01/01/2015 - 01/11/2020

| baseline closing value | index closing value | fees |
| --- | --- | --- |
| $496.83 | $409.55 | $18.47 |

### Implemented BCI rules

### Parameter description

### Support

If you like the package and you feel like you want to support its further development, then it will be of great help and most appreciated if you:
- file bugs, proposals, pull requests, ...
- spread the word
- donate an arbitrary tip
  * `BTC`: `3GJPT6H6WeuTWR2KwDSEN5qyJq95LEErzf`
  * `ETH`: `0xC7d8673Ee1B01f6F10e40aA416a1b0A746eaBe68`
