#!/bin/bash

# Unsorted temporary index to sorted form on disk
for file in ./indexfiles/unsortedchunks/*; do
    sort -S 75% $file -o "./indexfiles/sortedchunks/${file##*/}"
    echo "$file done"
done

sort -m ./sortedchunks/* | split -l 2000000 - mergedchunks_m/x
