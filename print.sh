#!/bin/bash

# Base directory to start from
base_dir="."

# Find all files in the directory and loop through them
find "$base_dir" -type f | while read -r file; do
    echo "File: $file"
    cat "$file"
    echo # add a blank line for better separation between file contents
done

