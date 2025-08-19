#!/usr/bin/env bash
set -euo pipefail

# -------------------- ZRAM Setup --------------------
# Configure and enable zram swap (compressed RAM disk)
if command -v zramctl >/dev/null 2>&1; then
    echo "Configuring zram swap..."
    ZRAM_SIZE="128M"
    zramctl --find --size $ZRAM_SIZE
    ZRAM_DEV=$(zramctl --list | awk 'NR==2{print $1}')
    if [ -n "$ZRAM_DEV" ]; then
        mkswap "$ZRAM_DEV"
        swapon "$ZRAM_DEV"
        echo "zram swap enabled on $ZRAM_DEV ($ZRAM_SIZE)"
    else
        echo "Failed to configure zram device" >&2
    fi
else
    echo "zramctl not found, skipping zram swap setup."
fi

declare -a SERVICE_PIDS=()

wait_for_port() {
    local port="$1"
    printf 'Waiting for localhost:%s/status ' "$port"
    until curl -sf "http://localhost:${port}/status" >/dev/null 2>&1; do
        sleep 1
        printf '.'
    done
    echo " ready!"
}

start_service() {
    local name="$1" path="$2" port="$3"
    echo "Starting ${name} on port ${port} ..."
    (cd "$path" && uvicorn xMain:app --host 0.0.0.0 --port "$port") &
    SERVICE_PIDS+=("$!")
    echo "${name} PID: $!"
    wait_for_port "$port"
}

start_nginx() {
    local port="$1"
    echo "Starting NGINX on port ${port} ..."
    nginx -g "daemon off;" &
    SERVICE_PIDS+=("$!")
    echo "NGINX PID: $!"
}

cleanup() {
    echo "Shutting down services ..."
    kill "${SERVICE_PIDS[@]}" 2>/dev/null || true
}
trap cleanup EXIT

start_service "BackEnd" "./BackEnd" 8001
start_nginx 8080

wait "${SERVICE_PIDS[@]}"