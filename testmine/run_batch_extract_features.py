#!/usr/bin/python

from matplotlib import pyplot
import caffe
import numpy as np
import os
import sys
import pdb

# Set the right path to your model file, pretrained model,
# and the image you would like to classify.
#MODEL_FILE = 'imagenet_deploy.prototxt'
#PRETRAINED = './caffe_reference_imagenet_model'


if len(sys.argv) < 4:
    print 'Usage: ./run_batch...py <MODEL_FILE> <PRETRAINED> <IMAGE_FILE_LIST> [device_id = 0 or 1]'
    sys.exit()
else:
    MODEL_FILE = sys.argv[1]
    PRETRAINED = sys.argv[2]

    IMAGE_FILE_LIST = sys.argv[3]
# caffe_root = '/home/qyou/src/caffe-release/caffe-0.999'    
caffe_root = '/home/jack/Documents/caffe'    


device_id = 0
if len(sys.argv) > 4:
    device_id = int(sys.argv[4])

#MODEL_FILE = 'lower_vso_deploy.prototxt'
#PRETRAINED = 'lower_vso_fseq_train_iter_70000'
#IMAGE_FILE = '/home/qyou/Downloads/lena.png'

net = caffe.Classifier(MODEL_FILE, PRETRAINED, mean_file=os.path.join(caffe_root , '/testmine/senti/flickr_vso.npy'),channel_swap=(2,1,0),input_scale=255)
net.set_phase_test()
net.set_mode_gpu()
net.set_device(device_id)

#prediction = net.predict(IMAGE_FILE)

fid = open(IMAGE_FILE_LIST,'r')

fail_fid = open('fail_imgs.txt','w')

pred_label = -1
for aline in fid:
    aline = aline.strip()
    input_images = []
    parts = aline.split()
    full_fn = parts[0]
    #predict this image using the pretrained model.
    try:
        input_image = caffe.io.load_image(full_fn)
        input_images.append(input_image)
    except:
        fail_fid.write(full_fn + '\n')
        fail_fid.flush()
        continue

    prediction = net.predict(input_images, oversample=False)
    fc7 = net.blobs['fc7'].data
    fc7 = np.reshape(fc7, (1,fc7.size))

    max_idx = np.argmax(fc7, axis=1)
    sys.stdout.write(full_fn +  ' ' + str(max_idx[0]))
    for j in range(fc7.shape[1]):
        sys.stdout.write(' ' + str(fc7[0][j]))
    sys.stdout.write('\n')
fail_fid.close()
        
