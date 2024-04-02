#!/bin/bash
SCRIPT_DIR=$(dirname -- "$0")
source $SCRIPT_DIR/vars.sh
python3 $SCRIPT_DIR/../json_PRO3X.py --ip $IP  --interval $INTERVAL --outlet $OUTLET --user $RF_USER --password $RF_PASSWORD --output $1/result.json &

echo "$!" > $1/power.pid
