#!/bin/bash

# Function to create CPU load
load_cpu() {
    while :; do :; done
}

# Duration of load and sleep times (adjust as necessary)
load_duration=0.4  # seconds
sleep_duration=0.6 # seconds

# Start the load in the background
while true; do
    # Start CPU load on 32 cores
    for i in $(seq 1 32); do
        load_cpu &
    done

    # Let it run for load_duration
    sleep $load_duration

    # Kill the CPU load
    pkill -f load_cpu

    # Sleep for sleep_duration
    sleep $sleep_duration
done
