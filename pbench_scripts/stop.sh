#!/bin/bash

kill `cat $1/power.pid`
rm $1/power.pid
