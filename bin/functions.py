from pyproj import Proj
import numpy as np
import pandas as pd
import dateutil
from scipy.spatial import cKDTree


def WTK_idx(wtk, lat_lon):
    """
    Function to find the nearest x/y WTK indices for a given lat/lon using
    Proj4 projection library

    Parameters
    ----------
    wtk : 'h5pyd.File'
        h5pyd File instance for the WTK
    lat_lon : tuple | list
        (lat, lon) coordinates of interest

    Results
    -------
    ij : 'tuple'
        x/y coordinate in the database of the closest pixel to coordinate of
        interest
    """
    dset_coords = wtk['coordinates']
    projstring = """+proj=lcc +lat_1=30 +lat_2=60
                    +lat_0=38.47240422490422 +lon_0=-96.0
                    +x_0=0 +y_0=0 +ellps=sphere
                    +units=m +no_defs """
    projectLcc = Proj(projstring)
    # Grab origin directly from database
    origin_ll = reversed(dset_coords[0][0])
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
        x/y coordinate in the database of the closest pixel to coordinate of
        interest
    """
    dset_coords = nsrdb['coordinates'][...]
    tree = cKDTree(dset_coords)
    _, pos = tree.query(np.array(lat_lon))
    return pos


def datetimeIndex(f):
    """
    Function returns a dataframe containing the time-dimension
    index and parsed timestamps

    Parameters
    ----------
    f : 'h5pyd.File'
        h5pyd File instance for the wtk_us.h5

    Results
    -------
    dt : 'pd.DataFrame'
        DataFrame containing parsed 'datetime' stamps
    """
    dt = f["datetime"]
    dt = pd.DataFrame({"datetime": dt[:]}, index=range(0, dt.shape[0]))
    dt['datetime'] = dt['datetime'].apply(dateutil.parser.parse)
    return dt


class HSDS:
    """
    HSDS Resource handler class
    """
    def __init__(self, hsds_path):
        """
        Parameters
        ----------
        hsds_path : h5pyd.File instance
        """
        self._h5d = h5pyd.File(hsds_path, mode='r')
        self._time_index = None
        self._meta = None
        self._tree = None

    @property
    def time_index(self):
        """
        Returns
        -------
        _time_index : pd.Datetime_Index
            Datetime index vector for given HSDS file
        """
        if self._time_index is None:
            time_index = self._h5d['time_index'][...].astype(str)
            self._time_index = pd.to_datetime(time_index)

        return self._time_index

    @property
    def meta(self):
        """
        Returns
        -------
        _meta : pd.DataFrame
            Site meta data for give HSDS file
        """
        if self._meta is None:
            self._meta = pd.DataFrame(self._h5d['meta'][...])

        return self._meta

    @property
    def tree(self):
        """
        Returns
        -------
        _tree : cKDTree
            KDTree on site coordinates (latitude, longitude)
        """
        if self._tree is None:
            site_coords = self._h5d['coordinates'][...]
            self._tree = cKDTree(site_coords)

        return self._tree

    def _nearest_site(self, coords):
        """
        Find nearest site to coordinate (lat, lon) of interest

        Parameters
        ----------
        coords : tuple
            (lat, lon) coordinates of interest

        Returns
        -------
        site_idx : int
            Site index in the datasets
        """
        lat_lon = np.array(coords)
        _, site_idx = self.tree.query(lat_lon)
        return site_idx

    def _nearest_timestep(self, timestep):
        """
        Find the nearest timestep to timestep of interest

        Parameters
        ----------
        timestep : datetime
            Datetime step of interest

        Returns
        -------
        time_idx : int
            Time index in the datasets
        """
        delta = np.abs(self.time_index - timestep)
        time_idx = delta.argmin()

        return time_idx

    def _get_region_idx(self, value, column='state'):
        """
        Find sites associated with given region

        Parameters
        ----------
        value : str
            Regional value filter to
        column : str
            Column in the meta data to filter on

        Returns
        -------
        region_idx : list
            Indices of all sites corresponding to region of interest
        """
        if column in self.meta:
            col_data = self.meta[column].str.decode('utf-8')
            region_idx = self.meta.index[col_data == value].values
        else:
            raise ValueError('{} is not a valid column in meta'
                             .format(column))

        return region_idx

    def _get_conus_idx(self):
        """
        Find sites associated with CONUS

        Returns
        -------
        conus_idx : list
            Indices of all sites in CONUS
        """
        country_data = self.meta['country'].str.decode('utf-8')
        us_idx = country_data == 'United States'
        state_data = self.meta.loc[us_idx, 'state'].str.decode('utf-8')
        conus_idx = state_data.isin(['Alaska', 'Hawaii', 'AK', 'HI', 'None'])
        conus_idx = state_data.index[~conus_idx].values

        return conus_idx

    def get_timeseries(self, variable, coords, local=True):
        """
        Extract time-series data for the given variable at the given
        coordinates

        Parameters
        ----------
        variable : str
            Variable to extract time-series for
        coords : tuple
            (lat, lon) coordinates of interest
        local : bool
            Shift time-series to local time

        Returns
        -------
        ts : pd.DataFrame
            Time-series DataFrame
        """
        site_idx = self._nearest_site(coords)
        time_index = self.time_index
        if local:
            utc_dt = self.meta.iloc[site_idx]['timezone']
            utc_dt = pd.Timedelta('{}h'.format(utc_dt))
            time_index += utc_dt

        ts = self._h5d[variable][:, site_idx]
        ts = pd.DataFrame({variable: ts, 'datetime': time_index,
                           'date': time_index.date, 'month': time_index.month,
                           'day': time_index.day, 'hour': time_index.hour})

        return ts

    def get_day(self, variable, date, local=True):
        """
        Extract a days worth of data for the given day for CONUS

        Parameters
        ----------
        variable : str
            Variable to extract time-series for
        date : str
            Date to extract a days worth of data for
        local : bool
            Shift time-series to local time

        Returns
        -------
        day : pd.DataFrame

        """
        region_idx = self._get_region_idx(state)
        time_index = self.time_index
        if local:
            utc_dt = self.meta.iloc[region_idx]['timezone'].mean()
            utc_dt = pd.Timedelta('{}h'.format(utc_dt))
            time_index += utc_dt

        date = pd.to_datetime(date).date()
        time_idx = np.where(time_index.date == date)[0]
        time_idx = slice(time_idx[0], time_idx[-1] + 1)

        day = self._h5d[variable][time_idx][:, region_idx]

        return day
