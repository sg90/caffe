for name in /home/jack/Documents/caffe/testmine/rem_imgs/*.jpg;
do
    # echo $name
    #str=`identify $name|grep "[0-9]\+x[0-9]\++0+0"`
    str=`identify $name`
    # echo $str
    convert -crop `python process1.py "$str"` $name $name
    # echo $str
done
