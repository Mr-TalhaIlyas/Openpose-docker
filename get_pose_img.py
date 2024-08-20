import sys
import cv2
import os
from sys import platform
import argparse
import pyopenpose as op
import matplotlib.pyplot as plt
params = dict()
params["model_folder"] = "/openpose/models/"
params["face"] = True
params["hand"] = True
params["write_json"] = "/openpose/output/" # to save the json file comment to not save

opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Process Image
datum = op.Datum()
imageToProcess = cv2.imread('/openpose/examples/media/COCO_val2014_000000000241.jpg')
datum.cvInputData = imageToProcess
opWrapper.emplaceAndPop(op.VectorDatum([datum]))

print("Body keypoints: \n" + str(datum.poseKeypoints))
print("Face keypoints: \n" + str(datum.faceKeypoints))
print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))

plt.imshow(datum.cvOutputData)
