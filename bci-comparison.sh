#!/bin/bash

for i in `seq 4 3 25`; do
    echo "Index size: $i"
    python bci-comparison.py --index $i | tee "$i.log" &
done