#!/usr/bin/env sh
python distribute/python/classify.py  --pretrained_model ../examples/imagenet/caffe_reference_imagenet_model --model_def ../examples/imagenet/imagenet_deploy.prototxt ../examples/images/cat.jpg out
