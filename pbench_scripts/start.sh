#!/bin/bash
SCRIPT_DIR=$(dirname -- "$0")
source $SCRIPT_DIR/vars.sh
python3 $SCRIPT_DIR/../PRO3Xmultiple.py --ip $IP  --interval $INTERVAL --outlet $OUTLET --user $RF_USER --passwd $RF_PASSWORD --output $1/result.json &

echo "$!" > $1/power.pid
