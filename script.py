#!/bin/bash

process_name="your_python_script.py"

process_pid=$(pgrep -f "$process_name")

if [ -n "$process_pid" ]; then
  echo "Killing Python process with PID $process_pid"
  kill "$process_pid"
  nohup python /path/to/script.py > /dev/null &
else
  echo "Python process is not running."
  nohup python /path/to/script.py > /dev/null &
fi
