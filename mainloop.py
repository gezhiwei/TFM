#!/usr/bin/env python

import cv2

# Datasets imports
import datasets.datasetloader
import datasets.grazptz1
import datasets.grazptz2
import datasets.pets091
import datasets.pets092
import datasets.pets093
import datasets.pets094
import datasets.pets095
import datasets.pets096
import datasets.pets097
import datasets.pets098
import datasets.pets099

# 3D geometry imports
import threedgeometry.frameretriever
import threedgeometry.retroprojection

# Gui imports
from gui import imshow
from gui import trackbar

# Background imports
from bgsubtraction import bgprocess

# Detection imports
from detection import detectionprocess


def initcameras():

    dataset = datasets.datasetloader.selectdataset()

    load_cmd = 'datasets.%s.loaddataset()' % dataset
    cameras = eval(load_cmd)  # execute whatever is inside the string

    cameras = threedgeometry.frameretriever.getnumcameras(cameras)

    return cameras


def initloop(cameras):

    frames = threedgeometry.frameretriever.getframes(cameras)
    #frames = threedgeometry.frameretriever.getundistortedframes(cameras)

    bg = bgprocess.getbgobject()
    bg_models = bgprocess.getbgmodels(frames, bg)

    # Init trackbars
    tb = trackbar.setdefaulttrackbarmain(bg)
    trackbar.setdefaulttrackbardsecondary(bg_models)

    return bg_models, tb


def loop():

    cameras = initcameras()

    bg_models, tb = initloop(cameras)

    while True:

        option = bg_models[0].bg.option  # get which img you want to visualize

        frames = threedgeometry.frameretriever.getframes(cameras)
        #frames = threedgeometry.frameretriever.getundistortedframes(cameras)

        if not frames:  # Video ended
            break

        bg_models = bgprocess.bgprocess(frames, bg_models)

        blobs = detectionprocess.detectionprocess(bg_models)

        # imshow options
        if option is 0:
            imshow.showallimg(frames)

        elif option is 1:
            imshow.showallimg(bgprocess.getbgimg(bg_models))

        elif option is 2:
            imshow.showallimg(bgprocess.getbinimg(bg_models))

        elif option is 3:
            imshow.showallimg(bgprocess.getscanimg(bg_models))

        elif option is 4:
            imshow.showallimg(bgprocess.getdiffimg(bg_models))

        elif option is 5:
            imshow.showallimg(imshow.paintcontours(frames, bg_models))

        elif option is 6:
            imshow.showallimg(imshow.paintblobs(frames, blobs))

        # show frames no video
        if tb.framebyframe is 1:
            cv2.waitKey()