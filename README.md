# Bitpanda Crypto Index Simulator

Bitpanda Crypto Index (BCI) is an index product offered by the Austrian crypto broker bitpanda. The index consits of preselected crypto assets based on their actual market capitalization and gets recalculated (rebalanced) monthly to reflect shifts in the market. For full description read the [prospectus](https://cdn.bitpanda.com/media/bci/Prospectus_Index_English.pdf).

This package serves to simulate BCI calculation, determine its composition and perform monthly rebalancing based on the historical input data in order to calculate yield and compare it with the returns resulting from holding the original assets without any rebalancing. This may help decide whether investing in the index is profitable or at least help compare performance with different parameters.

The package tries to simulate BCI rules as much as possible but this cannot be achieved 100% due to certain steps being not explicitly described in the prospectus and bitpanda reserving rights to potentially adjust the rules fully at their sole discretion. Nevertheless, outcome of the simulation still provides valuable insight into mechanics of the index and its evolution over time.

This simulator is highly configurable but it comes with readymade configuration scripts for `BCI5` and `BCI10` indices (see `bci5.sh` and `bci10.sh`).

Calculation is performed based on the historical data provided in JSON format. The repository already contains a sample input file `input_data.json` which contains prices, market capitalizations and volumes of all cryptocurrencies since 01/01/2015 up to 01/11/2020 as published by `CoinGecko`.

Disclaimer: I am by no means affiliated with bitpanda (though I have been their customer for a couple of years) and this project was developed for own purposes. 

### Examples

I will demonstrate `BCI5` simulation by executing `bci5.sh` for a period of two months with a single rebalancing and explain the output.

```bash
bci-simulator$ ./bci5.sh 
Bitpanda Crypto Index Simulator

Simulation period: 2020-10-01 - 2020-11-01

Initializing portfolio for $1000.0...
	Top 5 assets:
		('BTC', {'price': 10770.881347466415, 'cap': 196617081790.5188, 'volume': 18558607662.6852, 'volume_avg': 618620255.42284})
		('ETH', {'price': 359.59898475085777, 'cap': 39782583382.89109, 'volume': 8037484324.980594, 'volume_avg': 267916144.1660198})
		('XRP', {'price': 0.2413448305484734, 'cap': 10899063751.06877, 'volume': 1349173492.0133767, 'volume_avg': 44972449.73377922})
		('BCH', {'price': 227.4442224750153, 'cap': 4214806111.9247684, 'volume': 1951827124.3319783, 'volume_avg': 65060904.14439928})
		('DOT', {'price': 4.347197258520258, 'cap': 3998481295.7904816, 'volume': 131549097.16661954, 'volume_avg': 4384969.905553984})
	Percentage allocation according to capitalization:
		['BTC', 0.7695022903928511]
		['ETH', 0.15569750477476302]
		['XRP', 0.042655777632386496]
		['BCH', 0.01649552992625229]
		['DOT', 0.01564889727374705]
	Capped percentage allocation:
		['BTC', 0.35]
		['ETH', 0.35]
		['XRP', 0.1710788535725429]
		['BCH', 0.06615836131685422]
		['DOT', 0.06276278511060296]
Portfolio allocation: {'BTC': 0.032495019554024604, 'ETH': 0.9733064186554691, 'XRP': 708.8565070308487, 'BCH': 0.29087729992403616, 'DOT': 14.437528683013289}

Rebalancing 2020-11-01
	Primary filtering:
		BTC: value $: 10,421,794,299,498.244 (average volume: 756373349.3135134, price: 13778.637638352931)
		ETH: value $: 115,873,709,651.78224 (average volume: 300311869.1204272, price: 385.8445887975079)
		XRP: value $: 10,692,339.963186288 (average volume: 44616541.874634266, price: 0.23964967955674707)
		BCH: value $: 17,892,998,542.0472 (average volume: 68397980.41526909, price: 261.60126999967366)
		DOT: value $: 12,692,380.646972526 (average volume: 3037895.3923114613, price: 4.178017676018528)
		Preserved coins: ['BTC', 'ETH', 'XRP', 'BCH', 'DOT']
	Secondary filtering:
		LINK: value $: 349,656,122.9518303 (average volume: 31148194.075876944, price: 11.225566467836583)
		LTC: value $: 3,659,559,609.5017962 (average volume: 65691484.73552311, price: 55.708279760083805)
		ADA: value $: 1,138,191.1141385778 (average volume: 12255799.576950926, price: 0.09286959263589264)
		EOS: value $: 117,559,867.06228183 (average volume: 46529621.355682485, price: 2.5265597191008453)
		XMR: value $: 1,439,447,767.0476987 (average volume: 11403045.21180153, price: 126.23362797491573)
	Candidate list: ['BTC', 'ETH', 'XRP', 'BCH', 'DOT', 'LINK', 'LTC', 'ADA', 'EOS', 'XMR']
	Sorted candidate list:
		BTC:	254,260,250,527.50497
		ETH:	44,687,833,549.98935
		XRP:	10,856,481,131.012754
		BCH:	4,864,602,893.168462
		LINK:	4,386,318,369.521734
		DOT:	3,874,741,303.6816278
		LTC:	3,645,413,637.9691725
		ADA:	2,891,746,978.3344765
		EOS:	2,392,706,148.826251
		XMR:	2,247,877,179.831775
	Index composition: ['BTC', 'ETH', 'XRP', 'BCH', 'DOT']
	Percentage allocation according to capitalization:
		['BTC', 0.7981952974776573]
		['ETH', 0.14028782918314306]
		['XRP', 0.03408158439217728]
		['BCH', 0.015271373112264097]
		['DOT', 0.012163915834758269]
	Capped percentage allocation:
		['BTC', 0.35]
		['ETH', 0.35]
		['XRP', 0.16620603035651954]
		['BCH', 0.0744740700395752]
		['DOT', 0.05931989960390529]
	New portfolio allocation: {'BTC': 0.02869301922003787, 'ETH': 1.0246371882920944, 'XRP': 783.4015168786901, 'BCH': 0.3215731090962748, 'DOT': 16.03779352929636}
	Portfolio value: 1,129.5734702377083
	Portfolio updates: {'BTC': -0.003802000333986734, 'ETH': 0.051330769636625306, 'XRP': 74.54500984784147, 'BCH': 0.03069580917223863, 'DOT': 1.6002648462830695}
	Fee: 2.0954553961160016 USD
	Original portfolio value: 1,129.5734702377083

Overall fee: 2.0954553961160016

```

### Implemented BCI rules

### Parameter description

### Support

If you like the package and you feel like you want to support its further development, then it will be of great help and most appreciated if you:
- file bugs, proposals, pull requests, ...
- spread the word
- donate an arbitrary tip
  * `BTC`: `3GJPT6H6WeuTWR2KwDSEN5qyJq95LEErzf`
  * `ETH`: `0xC7d8673Ee1B01f6F10e40aA416a1b0A746eaBe68`
