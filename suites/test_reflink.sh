#!/bin/bash
set -e

DIR="/var/lib/mnemon"
if [ ! -w "$DIR" ]; then
    DIR="/tmp"
fi

echo "=== XFS Reflink Benchmark on $DIR ==="
SRC="$DIR/bench_cow_source_100mb.bin"
DST="$DIR/bench_cow_clone_100mb.bin"

echo "Creating 100MB block file..."
dd if=/dev/zero of="$SRC" bs=1M count=100 status=none

echo "Testing cp --reflink=always..."
for i in 1 2 3 4 5; do
    rm -f "$DST"
    START=$(date +%s%N)
    cp --reflink=always "$SRC" "$DST"
    END=$(date +%s%N)
    DIFF_MS=$(echo "scale=3; ($END - $START) / 1000000" | bc)
    echo "Run $i: ${DIFF_MS} ms"
done

echo "Testing normal copy..."
for i in 1 2; do
    rm -f "$DST"
    START=$(date +%s%N)
    cp "$SRC" "$DST"
    END=$(date +%s%N)
    DIFF_MS=$(echo "scale=3; ($END - $START) / 1000000" | bc)
    echo "Normal copy $i: ${DIFF_MS} ms"
done

rm -f "$SRC" "$DST"
echo "=== Done ==="
