#!/bin/bash
echo "=== Thanaton Isolate Micro-Sandbox Cold-Start Benchmark ==="
for i in 1 2 3 4 5; do
    START=$(date +%s%N)
    sudo isolate --cg -b 100 --init >/dev/null 2>&1
    sudo isolate --cg -b 100 --run -- /bin/echo OK >/dev/null 2>&1
    sudo isolate --cg -b 100 --cleanup >/dev/null 2>&1
    END=$(date +%s%N)
    DIFF_MS=$(echo "scale=3; ($END - $START) / 1000000" | bc)
    echo "Isolate Run $i: ${DIFF_MS} ms"
done

echo ""
echo "=== Docker Container Cold-Start Benchmark ==="
IMG=$(sudo docker images --format "{{.Repository}}:{{.Tag}}" | head -n 1)
if [ -z "$IMG" ]; then
    echo "No local docker image found, pulling alpine..."
    sudo docker pull alpine:latest
    IMG="alpine:latest"
fi
echo "Using Docker image: $IMG"
for i in 1 2 3 4 5; do
    START=$(date +%s%N)
    sudo docker run --rm "$IMG" /bin/echo OK >/dev/null 2>&1
    END=$(date +%s%N)
    DIFF_MS=$(echo "scale=3; ($END - $START) / 1000000" | bc)
    echo "Docker Run $i: ${DIFF_MS} ms"
done
echo "=== Done ==="
