# Jordan Perr-Sauer <jordan.perr-sauer@nrel.gov>
# December, 2017
# shape.py, script to help download WTK data in hsds server for points within geojson shape

GEOJSON_FILE = "../data/wtk/W0463_1kmBuffer.json"

DESTINATION = "./output"

DATASETS = ["windspeed_10m", "windspeed_40m", "windspeed_60m", "windspeed_80m", "windspeed_100m", "windspeed_120m",
            "winddirection_10m", "winddirection_10m", "winddirection_10m", "winddirection_10m", "winddirection_10m", "winddirection_10m",
            "temperature_2m", "temperature_10m", "temperature_100m", "temperature_120m",
            "pressure_0m", "pressure_100m",
            "relativehumidity_2m",
            "inversemoninobukhovlength_2m"]

SKIP = 1 # stride length in x and y

tmin = 0  # hours since 12AM January 1st, 2007
tmax = 5 # hours since 12AM January 1st, 2007

tskip = 1 # stride length in time

#################

import h5pyd
import geopandas as gpd
import numpy as np
from pyproj import Proj
from tqdm import tqdm
import matplotlib
matplotlib.use("Agg")


proj4j_string = """+proj=lcc +lat_1=30 +lat_2=60
                +lat_0=38.47240422490422 +lon_0=-96.0
                +x_0=0 +y_0=0 +ellps=sphere
                +units=m +no_defs """
projectLcc = Proj(proj4j_string)


# Download origin data from server

f = h5pyd.File("/nrel/wtk-us.h5", 'r')
dset_coords = f['coordinates']
origin_ll = reversed(dset_coords[0][0]) # Grab origin directly from database
origin = projectLcc(*origin_ll)

# Read polygon from GeoJSON and find IJ bounds

polygon = gpd.read_file(GEOJSON_FILE)
polygon.crs = {'init': 'epsg:4326'}
polygon_lcc = polygon.to_crs(proj4j_string)
bounds = polygon_lcc.scale(2,2).bounds.iloc[0]

ll = (bounds.minx, bounds.miny)
ur = (bounds.maxx, bounds.maxy)

delta = np.subtract(ll, origin)
ll_ij = [int(round(x/2000)) for x in delta]

delta = np.subtract(ur, origin)
ur_ij = [int(round(x/2000)) for x in delta]

# Download data from server and write to CSV file

coords = dset_coords[ll_ij[1]:ur_ij[1]:SKIP,ll_ij[0]:ur_ij[0]:SKIP]
coordsToString = np.vectorize(lambda c: "(%f %f)"%(c[0], c[1]))
np.savetxt("%s/coords.csv"%(DESTINATION), coordsToString(coords), fmt="%s", delimiter=",")

for d in tqdm(DATASETS, desc="Downloading Datasets"):
    data = f[d][tmin:tmax:tskip,ll_ij[1]:ur_ij[1]:SKIP, ll_ij[0]:ur_ij[0]:SKIP]
    for t in range(data.shape[0]):
        np.savetxt("%s/%s_t%d.csv"%(DESTINATION, d, t), data[t], fmt='%.18f', delimiter=",")

ax = polygon.plot()
x,y = zip(*coords.flatten())
ax.scatter(y,x,c='g')
fig = ax.get_figure()
fig.savefig("%s/plot.png"%(DESTINATION))