#!/usr/bin/python

import caffe
import numpy as np
import sys

if len(sys.argv) != 3:
    print "Usage: python convert_protomean.py mean.binaryproto out.npy"
    sys.exit()

blob = caffe.proto.caffe_pb2.BlobProto()
data = open( sys.argv[1] , 'rb' ).read()
blob.ParseFromString(data)
arr = np.array( caffe.io.blobproto_to_array(blob) )
print len(arr)
out = arr[0]
np.save( sys.argv[2] , out )
