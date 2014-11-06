i=0
filename=''
for name in `cat /home/jack/Documents/caffe/testmine/feature_extract/file_rem.txt`;
do
    # echo $name
    if [ $((i % 2)) = 1 ]; then
        # echo $i
        filename="$filename $name"
        # echo "$filename"
        cp "$filename" "./rem_imgs"
    else
        filename=$name
    fi
    
    i=`expr $i + 1`
done
