#!/bin/bash

process_name="python3"

process_pid=$(pgrep -f "$process_name")

if [ -n "$process_pid" ]; then
  echo "Killing Python process with PID $process_pid"
  kill "$process_pid"
  nohup python3 main.py > /dev/null 2>&1 &
else
  echo "Python process is not running."
  nohup python3 main.py > /dev/null 2>&1 &
fi
