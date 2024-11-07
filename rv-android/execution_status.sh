#!/bin/sh

memory_file_path="$1"
#results_dir="20241106080954"
#memory_file_path="/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/results/$results_dir/execution_memory.json"

if [ -z "$memory_file_path" ]; then
  echo "Please provide the path to the execution memory file."
  exit 1
fi

python execution_status.py "$memory_file_path"

