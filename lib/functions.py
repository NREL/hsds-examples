from pyproj import Proj
import numpy as np
import pandas as pd
import dateutil
from scipy.spatial import cKDTree


def WTK_idx(wtk, lat_lon):
    """
    Function to find the nearest x/y WTK indices for a given lat/lon using Proj4 projection library

    Parameters
    ----------
    wtk : 'h5pyd.File'
        h5pyd File instance for the WTK
    lat_lon : tuple | list
        (lat, lon) coordinates of interest

    Results
    -------
    ij : 'tuple'
        x/y coordinate in the database of the closest pixel to coordinate of interest
    """
    dset_coords = wtk['coordinates']
    projstring = """+proj=lcc +lat_1=30 +lat_2=60
                    +lat_0=38.47240422490422 +lon_0=-96.0
                    +x_0=0 +y_0=0 +ellps=sphere
                    +units=m +no_defs """
    projectLcc = Proj(projstring)
    origin_ll = reversed(dset_coords[0][0])  # Grab origin directly from database
    origin = projectLcc(*origin_ll)

    lon_lat = reversed(lat_lon)
    coords = projectLcc(*lon_lat)
    delta = np.subtract(coords, origin)
    ij = [int(round(x / 2000)) for x in delta]
    return tuple(reversed(ij))


def NSRDB_idx(nsrdb, lat_lon):
    """
    Function to find the NSRDB site index for a given lat/lon using a KDTree

    Parameters
    ----------
    nsrdb : 'h5pyd.File'
        h5pyd File instance for the NSRDB
    lat_lon : tuple | list
        (lat, lon) coordinates of interest

    Results
    -------
    ij : 'tuple'
        x/y coordinate in the database of the closest pixel to coordinate of interest
    """
    dset_coords = nsrdb['coordinates'][...]
    tree = cKDTree(dset_coords)
    dist, pos = tree.query(np.array(lat_lon))
    return pos


# This function returns a dataframe containing the time-dimension
# index and parsed timestamps
def datetimeIndex(f):
    dt = f["datetime"]
    dt = pd.DataFrame({"datetime": dt[:]},index=range(0,dt.shape[0]))
    dt['datetime'] = dt['datetime'].apply(dateutil.parser.parse)
    return dt
