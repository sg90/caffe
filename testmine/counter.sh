#!/bin/sh

if [ $# != 1 ]; then
    echo "Note: sh counter.sh [dir]"
    exit 0
fi

csvfile="senti.result"
echo "n,POS,NEG" > $csvfile

cnt=1

for dir in $1*; do
    # echo $dir
    if [ -d "$dir" ]; then
        result_dir="$dir/out"
        echo $result_dir
        pos=`grep "1$" "$result_dir/label.txt"|wc -l`
        neg=`grep "0$" "$result_dir/label.txt"|wc -l`

        echo "${cnt},${pos},${neg}" >> $csvfile
        #echo $cnt
        cnt=`expr $cnt + 1`
        if [ $pos = 0 -a $neg = 0 ]; then
            echo "no"
        else
            #echo $pos/$neg(` expr $pos / $neg `);
            echo $pos
            echo $neg
        fi
    fi
done
