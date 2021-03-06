#!/usr/bin/env python

"""
The scripts that compose this module contains a set of datasets
with its respective camera views. Each camera view contains its
calibration and its video.

The module also contains a routine to load each dataset.
"""

import ConfigParser as cp

from threedgeometry.camera import Camera
from var import variables
