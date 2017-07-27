#!/usr/bin/env bash

mynohup () {
    [[ "$1" = "" ]] && echo "usage: mynohup python_script" && return 0
    nohup python -u "$1" > "${1%.*}.log" 2>&1 < /dev/null &
}

mykill() {
    ps -ef | grep "$1" | grep -v grep | awk '{print $2}' | xargs kill
    echo "process "$1" killed"
}

mynohup head.py

parallel --no-notice --delay 0.2 -j 4 < test_connectivity.sh

mykill head.py
