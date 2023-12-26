#!/bin/bash

# Define the server hostnames to check
SERVER_HOSTNAMES=("server1" "server2" "server3" "server4" "server5")

# Define the maximum number of retries
MAX_RETRIES=10

# Function to check if a server is up
check_server() {
    for hostname in "${SERVER_HOSTNAMES[@]}"; do
        if ping -c 1 "$hostname" &> /dev/null; then
            return 0
        fi
    done
    return 1
}

# Wait for servers to be up
retries=0
until check_server; do
    retries=$((retries+1))
    if [ "$retries" -gt "$MAX_RETRIES" ]; then
        echo "Max retries reached. Servers might not be up."
        exit 1
    fi
    echo "Waiting for servers... (attempt $retries/$MAX_RETRIES)"
    sleep 10
done

# Once servers are up, start the client logic (e.g., node client.js)
node client.js
