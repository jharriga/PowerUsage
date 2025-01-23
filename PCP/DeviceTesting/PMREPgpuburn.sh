#!/bin/bash
# Script which attempts to quatify GPU Power Efficiency by varying
# the GPU Frequency while the 'gpu_burn stress test. 
# NOTE: the script doesnot modify the existing Power Cap
###################################################################

# Configure GPU Frequencies for the test runs
# MIN and MAX were hardcoded for Nvidia A100
min_freq=210
max_freq=1410
multiplier=2 

delay=15        # Fixed DELAY between INNER-LOOP runs
runtime=30      # runtime duration for each gpu-burn run
sampletime=3    # sample time for PMREP Metrics

# Define workload
executable="./gpu_burn"                     # adjust for your executable location
workload="${executable} ${runtime}"
parsing="| tac | grep -m 1 Gflop"          # specific to gpu_burn output
exec_str="${workload} ${parsing}"
echo "Workload: ${workload}"

# Verify workload is avalaible on the system
if [ ! -x "$executable" ]; then
  echo "File ${executable} is not found. Exiting"
  exit 1
fi

# OUTER Loop - vary GPU Frequency
# Initialize vars for first loop
loop_ctr=1
this_freq=$(( min_freq*loop_ctr ))

while [ $this_freq .lt. $max_freq ]; do
    echo "GPU Freq for this set of runs: ${this_freq}"
    # Apply GPU Frequency
    nvidia-smi -lgc $min_freq,$this_freq

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
##        $exec_str &> /dev/null     # Record GFLOPS for the run
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
    
    # Initialize vars for next loop. Bail if you exceed MAX_FREQ
    ((loop_ctr++))
    this_freq=$(( min_freq*loop_ctr )) 
done
