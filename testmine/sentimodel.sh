#!/usr/bin/env sh
python ../python/classify.py  --images_dim 256,256 --pretrained_model ./senti/model_new --model_def ./senti/model4_boost_deploy.prototxt --mean_file ./senti/mean_new.npy ./senti/ out_senti
