# Jordan Perr-Sauer <jordan.perr-sauer@nrel.gov>

import h5pyd
import numpy as np
from pyproj import Proj
import sys

######### CONFIGURATION #########

lat = 36.96744946416934
lon = -109.05029296875
hub_height = "100"

#################################

f = h5pyd.File("/nrel/wtk-us.h5", 'r')

projstring = """+proj=lcc +lat_1=30 +lat_2=60
                +lat_0=38.47240422490422 +lon_0=-96.0
                +x_0=0 +y_0=0 +ellps=sphere
                +units=m +no_defs"""

projectLcc = Proj(projstring)

_origin_ll = reversed(f['coordinates'][0][0])  # Grab origin directly from database
origin = projectLcc(*_origin_ll)

def ijForCoord(coords):
    coords = reversed(coords)
    coords = projectLcc(*coords)
    delta = np.subtract(coords, origin)
    ij = [int(round(x/2000)) for x in delta]
    return tuple(reversed(ij))

i, j = ijForCoord((lat, lon))

coord = f["coordinates"][i][j]
speed = f["windspeed_{0}m".format(hub_height)][0:24,i,j]
direc = f["winddirection_{0}m".format(hub_height)][0:24,i,j]

### Write raw data

stack = np.column_stack((speed, direc))
np.savetxt('rawdata.out', stack, delimiter=",", fmt="%10.5f")

### Write
