#!/bin/sh

if [ $# != 1 ]; then
    echo "Note: sh run.sh [dir]"
    exit 0
fi

for dir in $1*; do
    # echo $dir
    if [ -d "$dir" ]; then
        output_dir="$dir/out"
        # echo $output_dir
        [ -d "$output_dir" ] || mkdir "$output_dir"
        # echo $dir
        python distribute/python/classify_m.py "$dir" "--output_file" "$output_dir"
    fi
done
