#!/usr/bin/env python

import cv2
import time
import datasets.datasetloader
"""
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
import datasets.oxtown
import datasets.caviar01
import datasets.caviar02
import datasets.caviar03
import datasets.caviar04
import datasets.caviar05
"""
import datasets.pets01_crop
import datasets.pets091
import datasets.ewap01
import datasets.oxtown
import datasets.grazptz1
import datasets.pets094
import datasets.pets095

import threedgeometry.frameretriever
import threedgeometry.retroprojection

from gui import imshow
from gui import trackbar

from bgsubtraction import bgprocess

from detection import detectionprocess

from tracker import trackerprocess

frame_num = 0

def initcameras():

    dataset = datasets.datasetloader.selectdataset()

    load_cmd = 'datasets.%s.loaddataset()' % dataset
    print load_cmd
    cameras, configuration = eval(load_cmd)

    cameras = threedgeometry.frameretriever.getnumcameras(cameras)

    return cameras, configuration

#initloop returns 'tracks' = an empty list to be filled in loop() @cia
def initloop(cameras, configuration):

    frames = threedgeometry.frameretriever.getbg(cameras)

    bg = bgprocess.getbgobject(configuration['global'])
    bg_models = bgprocess.getbgmodels(frames, bg, configuration, cameras)

    # Init trackbars
    tb = trackbar.setdefaulttrackbarmain(bg)
    trackbar.setdefaulttrackbardsecondary(bg_models)

    tracks = trackerprocess.inittracks(len(cameras))

    return bg_models, tb, tracks
    #RETURN 'tracks' is an empty list to be filled in mainloop() @cia

def saveframes(section, frames):
    global frame_num
    frame_num += 1
    for ii in range(len(frames)):
        cv2.imwrite("frames/%s_%s_%s.jpg" % (section, ii, frame_num), frames[ii])


def loop():

    cameras, configuration = initcameras()

    bg_models, tb, tracks = initloop(cameras, configuration)

    n_frames = 0.
    total_time = 0.

    while True:
        """
        print ''  # Debug purposes
        print '######################'
        print '       NEW FRAME'
        print '######################'
        print ''
        """

        program_starts = time.time()

        option = bg_models[0].bg.option  # get which img you want to visualize

        frames = threedgeometry.frameretriever.getframes(cameras)
        #frames = threedgeometry.frameretriever.getundistortedframes(cameras)

        if not frames:  # Video ended
            break
        #subjects = detectionprocess.hogdetectionprocess(frames)
        bg_models = bgprocess.bgprocess(frames, bg_models)
        
        blobs, subjects = detectionprocess.detectionprocess(bg_models, cameras, frames)

        tracks = trackerprocess.trackerprocess(tracks, subjects)

        # imshow options
        if option is 0:
            imshow.showallimg(frames)
            #saveframes('1_original', frames)

        elif option is 1:
            imshow.showallimg(bgprocess.getbgimg(bg_models))

        elif option is 2:
            imshow.showallimg(bgprocess.getbinimg(bg_models))
            #saveframes('2_f1', bgprocess.getbinimg(bg_models))

        elif option is 3:
            imshow.showallimg(bgprocess.getscanimg(bg_models))
            #saveframes('3_fm', bgprocess.getscanimg(bg_models))

        elif option is 4:
            imshow.showallimg(bgprocess.getdiffimg(bg_models))
            #saveframes('4_fc', bgprocess.getdiffimg(bg_models))

        elif option is 5:
            imshow.showallimg(imshow.paintcontours(frames, bg_models))
            #saveframes('5_blobs', imshow.paintcontours(frames, bg_models))

        elif option is 6:
            imshow.showallimg(imshow.paintblobs(frames, blobs))
            #saveframes('6_projection', imshow.paintblobs(frames, blobs))

        elif option is 7:
            imshow.showallimg(imshow.paint3dworld(frames, cameras))
            #imshow.showallimg(imshow.paintmasks(frames, blobs))
             
        elif option is 8:
            imshow.showallimg(imshow.paintsubjectsboxes(frames, subjects))
            #saveframes('d', frames)

        elif option is 9:
            imshow.showallimg(imshow.painttracks(frames, tracks))
            #saveframes('tracking', frames)
        
        now = time.time()
        #print("It has been {0} seconds since the loop started".format(now - program_starts))

        # show frames no video
        if tb.framebyframe is 1:
            cv2.waitKey()

        cv2.waitKey(bg_models[0].bg.waitkey)

        total_time += now - program_starts
        n_frames += 1   

        """
        if n_frames > 50:
            break 
        """

    print "mean performance time: %s fps: %s" % (total_time/n_frames, 1./(total_time/n_frames))

    datasets.datasetloader.saveconfiguration(cameras, configuration, bg_models)
