#!/bin/bash

python bci-simulator.py \
--index 5 \
--rebalancing 0 \
--fee 0.02 \
--max-allocation 0.35 \
--volume-period 30 \
--primary-volume-filter 600000 \
--secondary-volume-filter 1000000 \
--candidates 10 \
--primary-candidates 3 \
--secondary-candidates 7 \
--funds 1000 \
--offset 5 \
--input-file "input_data.json" \
--start-date "2017-12-01"