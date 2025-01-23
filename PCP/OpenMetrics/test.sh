#!/bin/bash
# Echo's Redfish Chassis & PDU power readings to screen, without using Perf CoPilot
# Requires vars in 'RFvars.cfg' to be configured for URLs and Credentials

while true; do
    # Emit timestamp
    echo
    date

    # Get Readings - CHASSIS
    ./RFchassis.sh

    # Get Readings - PDU1
    ./RFpdu1.sh

    # Get Readings - PDU2
    ./RFpdu2.sh

    # DELAY
    sleep 5
done
