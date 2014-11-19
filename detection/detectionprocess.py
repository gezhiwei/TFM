#!/usr/bin/env python

from detection import blob
from detection import cv2
from detection import np
from detection import subject


def contourstoblobs(bg_models):

    total_blobs = []

    for bg in bg_models:

        bin_img = bg.diff_img_copy
        bg_blobs = []

        for ii in range(len(bg.contours)):

            x, y, w, h = bg.rectangles[ii]

            b = blob.Blob()
            b.setdefault(
                bin_img[y:y + h, x:x + w],
                bg.rectangles[ii],
                bg.contours[ii])

            bg_blobs.append(b)

        total_blobs.append(bg_blobs)

    return total_blobs


def createglobalmask(total_blobs, bg_models):

    size = bg_models[0].bg_img.shape
    height = size[0]
    width = size[1]

    total_masks = []

    for bg_blobs in total_blobs:

        global_mask = np.zeros((height, width), dtype=np.uint8)

        for blob in bg_blobs:

            blob.drawglobalmask(global_mask)

        total_masks.append(global_mask)

    return total_masks


def globalmasktosubjects(total_masks, bg_models):

    total_subjs = []

    win_width = bg_models[0].win_width
    win_height = bg_models[0].win_height

    for mask in total_masks:

        subjs = []

        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cont in contours:

            x, y, w, h = cv2.boundingRect(cont)
            box = [x, y, w, h]

            if w >= (win_width / 2) and h >= (win_height / 2):

                rot_box = cv2.fitEllipse(cont)
                subj = subject.Subject()
                subj.setdefault(mask, box, rot_box)
                subjs.append(subj)

        total_subjs.append(subjs)

    return total_subjs


def detectionprocess(bg_models):

    total_blobs = contourstoblobs(bg_models)
    total_masks = createglobalmask(total_blobs, bg_models)
    total_subjs = globalmasktosubjects(total_masks, bg_models)

    return total_blobs, total_subjs
