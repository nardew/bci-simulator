#!/bin/bash

python bci-simulator.py \
--index 22 \
--rebalancing 180 \
--fee 0.02 \
--max-allocation 0.35 \
--volume-period 20 \
--primary-volume-filter 1500000 \
--secondary-volume-filter 2000000 \
--candidates 44 \
--primary-candidates 3 \
--secondary-candidates 8 \
--funds 1000 \
--offset 0 \
--input-file "input_data.json" \
--start-date "2016-01-01" \
--end-date "2020-11-01"