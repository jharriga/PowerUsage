#!/bin/bash

# Fixed DELAY between INNER-LOOP runs
delay=15

# OUTER Loop - increase $duration
duration=10
for multiplier in {1..4}; do
    this_dur=$((duration*multiplier))
    echo "Delay between samples: ${this_dur} seconds"
    load="openssl speed -evp sha256 -bytes 16384 -seconds ${this_dur} \
          -multi $(nproc)"
    echo "Workload: ${load}"
    fname="${this_dur}sec.csv"

    # Start PMREP in backgrd and record PID
    pmrep -t 3 -o csv -F ${fname} \
        openmetrics.RFchassis openmetrics.RFpdu1 openmetrics.RFpdu2 \
        denki.rapl openmetrics.kepler.kepler_node_platform_joules_total \
        openmetrics.control.fetch_time &
    pmrepPID=$!
    
    # INNER Loop - repeat for 5 samples 
    echo -n "Sample "
    for sample_ctr in {1..5}; do
        echo -n "${sample_ctr}, "
        sleep $delay
##        $load &> /dev/null
    done
# Terminate PMREP. Force flush buffers by using SIGUSR1 signal 
    kill -SIGUSR1 ${pmrepPID}
    echo; echo "------------------"

    if [ -e $fname ]; then
        echo "Succesfully created $fname"
    else
        echo "Failed to create $fname, exiting"
        exit 1
    fi
done

