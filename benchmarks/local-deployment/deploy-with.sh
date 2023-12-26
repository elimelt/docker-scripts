#!/bin/bash

# array to store PIDs of spawned processes
declare -a pids

# cleanup and kill all spawned processes
cleanup() {
    echo "Cleaning up..."
    for pid in "${pids[@]}"; do
        echo "Killing process $pid"
        kill -9 "$pid" >/dev/null 2>&1
    done
    exit 0
}

# trap EXIT signal to call cleanup
trap cleanup EXIT

# check num args
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number_of_servers>"
    exit 1
fi

n=$1

# define port range for servers
SERVER_PORT_START=3006
SERVER_PORT_END=$((SERVER_PORT_START + $1 - 1))

# set env variables
export SERVER_PORT_START
export SERVER_PORT_END


# start server processes
for (( i=1; i<=$n; i++ )); do
    echo "Starting server $i..."
    SERVER_NUMBER=$i node ./server/server.js &
    pids+=($!)

    # sleep 1
done

# start client processes
for (( i=1; i<=5; i++ )); do
    echo "Starting client $i..."
    CLIENT_NUMBER=$i node ./client/client.js &
    pids+=($!)

    # sleep 1
done

echo "Load testing started with $n servers and 5 clients."

# keep script running
wait
