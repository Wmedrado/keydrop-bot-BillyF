#!/bin/bash
set -e
mkdir -p build_results

CONTAINER_NAME="staging_bot"

# Remove previous container if any
if docker ps -a --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
  docker rm -f "$CONTAINER_NAME" || true
fi

# Remove previous image if any
if docker images -q "$CONTAINER_NAME" > /dev/null; then
  docker rmi -f "$CONTAINER_NAME" || true
fi

# Build image
docker build -t "$CONTAINER_NAME" .

# Run container detached with debug variables
docker run -d --name "$CONTAINER_NAME" \
  -e BOT_DEBUG=1 \
  -e LOG_CHANNEL=staging \
  "$CONTAINER_NAME"

# Run for three minutes
sleep 180

# Collect logs
mkdir -p build_results

docker logs "$CONTAINER_NAME" > build_results/staging_logs.txt || true

# Check for critical errors
if grep -i "CRITICAL" build_results/staging_logs.txt; then
  echo "Critical error found in staging logs"
  docker rm -f "$CONTAINER_NAME"
  exit 1
fi

# Clean up
docker rm -f "$CONTAINER_NAME"

echo "Staging run completed" > build_results/staging_status.log
