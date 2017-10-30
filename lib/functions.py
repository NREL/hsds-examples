from pyproj import Proj
import numpy as np
import pandas as pd
import dateutil

# This function finds the nearest x/y indices for a given lat/lon.
# Rather than fetching the entire coordinates database, which is 500+ MB, this
# uses the Proj4 library to find a nearby point and then converts to x/y indices
def indicesForCoord(f, lat_index, lon_index):
    dset_coords = f['coordinates']
    projstring = """+proj=lcc +lat_1=30 +lat_2=60 
                    +lat_0=38.47240422490422 +lon_0=-96.0 
                    +x_0=0 +y_0=0 +ellps=sphere 
                    +units=m +no_defs """
    projectLcc = Proj(projstring)
    origin_ll = reversed(dset_coords[0][0])  # Grab origin directly from database
    origin = projectLcc(*origin_ll)
    
    coords = (lon_index,lat_index)
    coords = projectLcc(*coords)
    delta = np.subtract(coords, origin)
    ij = [int(round(x/2000)) for x in delta]
    return tuple(reversed(ij))

# This function fetches the 7-year timeseries in chunks of 8,000 elements
def entireTimeseries(dset, lat_index, lon_index):
    extent = dset.shape[0]
    tseries = np.zeros((extent,), dtype=dset.dtype)
    items_per_req = 8000 # extract time series in batches of 8000 elements
    count = (extent // items_per_req) + 1
    for i in range(count):
        start = i*items_per_req
        stop = start + items_per_req
        if stop > extent:
            stop = extent
        tseries[start:stop] = dset[start:stop, lat_index, lon_index ]
    return tseries

# This function returns a dataframe containing the time-dimension 
# index and parsed timestamps
def datetimeIndex(f):
    dt = f["datetime"]
    dt = pd.DataFrame({"datetime": dt[:]},index=range(0,dt.shape[0]))
    dt['datetime'] = dt['datetime'].apply(dateutil.parser.parse)
    return dt