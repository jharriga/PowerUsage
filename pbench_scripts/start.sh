#!/bin/bash
SCRIPT_DIR=$(dirname -- "$0")
source $SCRIPT_DIR/vars.sh
python3 $SCRIPT_DIR/../json_PRO3X.py --ip $IP  --interval $INTERVAL --outlet $OUTLET --output $1/result &

echo "$!" > $1/power.pid
