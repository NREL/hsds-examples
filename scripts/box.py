# Jordan Perr-Sauer <jordan.perr-sauer@nrel.gov>

import h5pyd, h5py
import numpy as np
from pyproj import Proj
import sys

######### CONFIGURATION #########


output="output_file.hdf5"

# Rectangle in lat/lon
sw = [36.96744946416934, -109.05029296875]
ne = [41.02964338716638, -102.0849609375]

# Time coordinates (hours since 0:0:0 on January 1st, 2007)
tmin = 0
tmax = 24

# Full resolution would be 1,1,1
latskip = 1
lonskip = 1
tskip = 1

# Which data sets do you want included in the download?
datasets = ['windspeed_100m', 'winddirection_100m']


######### END CONFIGURATION #########

projstring = """+proj=lcc +lat_1=30 +lat_2=60
                +lat_0=38.47240422490422 +lon_0=-96.0
                +x_0=0 +y_0=0 +ellps=sphere
                +units=m +no_defs """
projectLcc = Proj(projstring)

f = h5pyd.File("/nrel/wtk-us.h5", 'r')

dset_coords = f['coordinates']
origin_ll = reversed(dset_coords[0][0]) # Grab origin directly from database
origin = projectLcc(*origin_ll)

def indicesForCoord(lat_index, lon_index):
    coords = (lon_index,lat_index)
    coords = projectLcc(*coords)
    delta = np.subtract(coords, origin)
    ij = [int(round(x/2000)) for x in delta]
    return tuple(reversed(ij))

def line(lat1, lon1, lat2, lon2):
    z = zip( np.linspace(lat1, lat2, 5000), np.linspace(lon1, lon2, 5000) )
    if sys.version_info >= (3,0):
        z = list(z)
    return z

def bounding_ij(sw, ne):
    bb = line(sw[0], ne[1], ne[0], ne[1]) #top
    bb.extend( line(sw[0], sw[1], ne[0], sw[1]) ) #bottom
    bb.extend( line(sw[0], sw[1], sw[0], ne[1]) ) #left
    bb.extend( line(ne[0], sw[1], ne[0], ne[1]) ) #right
    lcbb = map(lambda c: indicesForCoord(*c), bb)
    if sys.version_info >= (3,0):
        lcbb = list(lcbb)
    lcbb_i = [x[0] for x in lcbb]
    lcbb_j = [x[1] for x in lcbb]
    ne = (max(lcbb_i), max(lcbb_j))
    sw = (min(lcbb_i), min(lcbb_j))
    return (ne, sw)

bd = bounding_ij(sw, ne)


# Download data and save to local file

lf = h5py.File(output, "w")

for d in datasets:
    ds = f[d][tmin:tmax:tskip,bd[1][0]:bd[0][0]:latskip,bd[1][1]:bd[0][1]:lonskip]
    lf[d] = ds

lf["coordinates"] = f["coordinates"][bd[1][0]:bd[0][0]:latskip,bd[1][1]:bd[0][1]:lonskip]
lf.flush()
lf.close()
