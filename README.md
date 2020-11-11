# Bitpanda Crypto Index Simulator

Bitpanda Crypto Index (BCI) is an index product offered by the Austrian crypto broker bitpanda. The index consits of preselected crypto assets based on their actual market capitalization and gets recalculated (rebalanced) monthly to reflect shifts in the market. For full description read the [prospectus](https://cdn.bitpanda.com/media/bci/Prospectus_Index_English.pdf).

This package serves to simulate BCI calculation, determine its composition and perform monthly rebalancing based on the historical input data in order to calculate yield and compare it with the returns resulting from holding the original assets without any rebalancing. This may help decide whether investing in the index is profitable or at least help compare performance with different parameters.

The package tries to simulate BCI rules as much as possible but this cannot be achieved 100% due to certain steps being not explicitly described in the prospectus and bitpanda reserving rights to potentially adjust the rules fully at their sole discretion. Nevertheless, outcome of the simulation still provides valuable insight into mechanics of the index and its evolution over time.

This simulator is highly configurable but it comes with readymade configuration scripts for `BCI5` and `BCI10` indices (see `bci5.sh` and `bci10.sh`).

Calculation is performed based on the historical data provided in JSON format. The repository already contains a sample input file `input_data.json` which contains prices, market capitalizations and volumes of all cryptocurrencies since 01/01/2015 up to 01/11/2020 as published by `CoinGecko`.