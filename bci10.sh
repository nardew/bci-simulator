#!/bin/bash

python bci-simulator.py \
--index 10 \
--rebalancing 0 \
--fee 0.02 \
--max-allocation 0.3 \
--volume-period 30 \
--primary-volume-filter 600000 \
--secondary-volume-filter 1000000 \
--candidates 20 \
--primary-candidates 7 \
--secondary-candidates 13 \
--funds 1000 \
--input-file "input_data.json" \
--start-date "2020-01-01" \
