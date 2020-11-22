#!/bin/bash

python bci-simulator.py \
--index 5 \
--rebalancing 0 \
--fee 0.02 \
--max-allocation 1 \
--volume-period 30 \
--primary-volume-filter 0 \
--secondary-volume-filter 0 \
--candidates 10 \
--primary-candidates 0 \
--secondary-candidates 0 \
--funds 1000 \
--offset 0 \
--input-file "input_data.json" \
--start-date "2016-01-01" \
--end-date "2020-11-01" \
--bypass-validation