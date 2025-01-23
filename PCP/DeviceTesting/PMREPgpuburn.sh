#!/bin/bash
# Run with existing Power Cap

# define workload
workload="./gpu_burn ${runtime}"
echo "Workload: ${workload}"
    
delay=15        # Fixed DELAY between INNER-LOOP runs
runtime=30      # runtime duration for each gpu-burn run
sampletime=3    # sample time for PMREP Metrics

# OUTER Loop - vary GPU Frequency
freq_array=
for multiplier in {1..4}; do
    this_freq=$((duration*multiplier))   *REDO*
    echo "GPU Freq for these runs: ${this_freq}"
    # Apply GPU Frequency
    nvidia-smi -lgc $this_freq,$this_freq

    fname="${this_freq}sec.csv"

    # Start PMREP in backgrd and record PID
    pmrep -t ${sampletime} -o csv -F ${fname} \
        openmetrics.RFchassis openmetrics.RFpdu1 openmetrics.RFpdu2 \
        denki.rapl openmetrics.kepler.kepler_node_platform_joules_total \
        openmetrics.control.fetch_time &
    pmrepPID=$!

    # Is a SYNC point required to ensure PMREP is ready?
    
    # INNER Loop - repeat for 5 samples 
    echo -n "Sample "
    for sample_ctr in {1..5}; do
        echo -n "${sample_ctr}, "
        sleep $delay
##        $workload &> /dev/null
    done
# Terminate PMREP. Flush buffers by sendng SIGUSR1 signal 
    kill -SIGUSR1 ${pmrepPID}
    echo; echo "------------------"

    if [ -e $fname ]; then
        echo "Succesfully created $fname"
    else
        echo "Failed to create $fname, exiting"
        exit 1
    fi
done
