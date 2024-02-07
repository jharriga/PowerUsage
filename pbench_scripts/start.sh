#!/bin/bash
SCRIPT_DIR=$(dirname -- "$0")
python3 $SCRIPT_DIR/../json_PRO3X.py --ip 10.27.242.2 --interval 5 --outlet 3 --output $1/result.json &
echo "$!" > $1/power.pid
