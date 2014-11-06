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
        help="Input image, directory, or npy."
    )
    parser.add_argument(
        "--output_file",
        default = './out',
        help="Output npy filename."
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
        default='png|jpg|bmp',
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

    imgfiles = []
    inputs = []
    args.input_file = os.path.expanduser(args.input_file)
    if args.input_file.endswith('npy'):
        inputs = np.load(args.input_file)
    elif os.path.isdir(args.input_file):
        for ext in args.ext.split('|'):
            for im_f in glob.glob(args.input_file + '/*.' + ext):
                inputs.append(caffe.io.load_image(im_f))
                idx = im_f.rfind('/')
                imgfiles.append(im_f[idx + 1:])
    else:
        inputs = [caffe.io.load_image(args.input_file)]

    print "Classifying %d inputs." % len(inputs)

    # Classify.
    SIZE_NUM = 10
    start = time.time()
    input_len = len(inputs)
    reminder = input_len % SIZE_NUM
    group = input_len / SIZE_NUM
    predictions = classifier.predict(inputs[:reminder], not args.center_only)
    for i in range(group):
        predictions = np.concatenate((predictions, classifier.predict(inputs[reminder + i * SIZE_NUM : reminder + (i + 1) * SIZE_NUM], not args.center_only)))

    print "Done in %.2f s." % (time.time() - start)

    # Save
    # np.save(args.output_file, predictions)
    np.save(args.output_file + '/outfile', predictions)
    
    outfile = open(args.output_file + '/label.txt', 'w')
    for i in range(len(imgfiles)):
        img = imgfiles[i]
        prediction = predictions[i]
        label = 0
        if prediction[0] < prediction[1]:
            label = 1

        #print img, ":", prediction, ",", label
        outfile.write("%s\t%d\n" % (img, label))
    
    outfile.close()

if __name__ == '__main__':
    main(sys.argv)
