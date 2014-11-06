for name in senti/featureimg/*.jpg;
    do convert -resize 256x256\! $name $name
done
