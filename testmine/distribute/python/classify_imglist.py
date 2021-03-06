#!/usr/bin/env python
"""
classify.py is an out-of-the-box image classifer callable from the command line.

By default it configures and runs the Caffe reference ImageNet model.
"""
import numpy as np
import os
import sys
import argparse
import glob
import time

import caffe


def main(argv):
    pycaffe_dir = os.path.dirname(__file__)

    parser = argparse.ArgumentParser()
    # Required arguments: input and output files.
    parser.add_argument(
        "input_file",
        help="Input imagelist file."
    )
    parser.add_argument(
        "output_file",
        help="Output feature filename."
    )
    # Optional arguments.
    parser.add_argument(
        "--model_def",
        default=os.path.join(pycaffe_dir,
                "../../senti/model4_boost_deploy.prototxt"),
        help="Model definition file."
    )
    parser.add_argument(
        "--pretrained_model",
        default=os.path.join(pycaffe_dir,
                "../../senti/model_new"),
        help="Trained model weights file."
    )
    parser.add_argument(
        "--gpu",
        action='store_true',
        help="Switch for gpu computation."
    )
    parser.add_argument(
        "--center_only",
        action='store_true',
        help="Switch for prediction from center crop alone instead of " +
             "averaging predictions across crops (default)."
    )
    parser.add_argument(
        "--images_dim",
        default='256,256',
        help="Canonical 'height,width' dimensions of input images."
    )
    parser.add_argument(
        "--mean_file",
        default=os.path.join(pycaffe_dir,
                             '../../senti/mean_new.npy'),
        help="Data set image mean of H x W x K dimensions (numpy array). " +
             "Set to '' for no mean subtraction."
    )
    parser.add_argument(
        "--input_scale",
        type=float,
        help="Multiply input features by this scale to finish preprocessing."
    )
    parser.add_argument(
        "--raw_scale",
        type=float,
        default=255.0,
        help="Multiply raw input by this scale before preprocessing."
    )
    parser.add_argument(
        "--channel_swap",
        default='2,1,0',
        help="Order to permute input channels. The default converts " +
             "RGB -> BGR since BGR is the Caffe default by way of OpenCV."
    )
    parser.add_argument(
        "--ext",
        default='jpg',
        help="Image file extension to take as input when a directory " +
             "is given as the input file."
    )
    args = parser.parse_args()

    image_dims = [int(s) for s in args.images_dim.split(',')]

    mean, channel_swap = None, None
    if args.mean_file:
        mean = np.load(args.mean_file)
    if args.channel_swap:
        channel_swap = [int(s) for s in args.channel_swap.split(',')]

    # Make classifier.
    classifier = caffe.Classifier(args.model_def, args.pretrained_model,
            image_dims=image_dims, gpu=args.gpu, mean=mean,
            input_scale=args.input_scale, raw_scale=args.raw_scale,
            channel_swap=channel_swap)

    if args.gpu:
        print 'GPU mode'

    # Load numpy array (.npy), directory glob (*.jpg), or image file.

    

    fid = open(args.input_file,'r')
    fout = open(args.output_file, 'w')

    fail_fid = open('fail_imgs.txt','w')

    # Classify and Extraction.
    start = time.time()
    idnum = 0
    for aline in fid:
        aline = aline.strip()
        input_images = []
        parts = aline.split()
        full_fn = parts[0]
        try:
            input_image = caffe.io.load_image(full_fn)
            input_images.append(input_image)
            idnum += 1
        except:
            fail_fid.write(full_fn + '\n')
            fail_fid.flush()
            continue

        predictions = classifier.predict(input_images, not args.center_only)
        prediction = predictions[0]
        label = 0
        if prediction[0] < prediction[1]:
            label = 1
    
        idx = full_fn.rfind('/')
        if idx != -1:
            imgname = full_fn[idx + 1:]
        else:
            imgname = full_fn

        fout.write("%s\t%d\n" % (imgname, label))
        if idnum % 100 == 0:
            print "%d inputs have finished." % idnum
            fout.flush()

    fid.close()
    fail_fid.close()
    fout.close()
    
    print "Classifying %d inputs." % idnum
    print "Done in %.2f s." % (time.time() - start)

if __name__ == '__main__':
    main(sys.argv)
