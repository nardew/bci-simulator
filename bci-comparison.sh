#!/bin/bash

for i in `seq 4 5 31`; do
    echo "Index size: $i"
    python bci-comparison.py --index $i | tee "$i.log" &
done