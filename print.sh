#!/bin/bash

base_dir="."

find "$base_dir" -type f | while read -r file; do
    echo "File: $file"
    cat "$file"
    echo
done

