# Solar Resource Data: National Solar Radiation Database (NSRDB)

/nrel/nsrdb/

## NSRDB

The National Solar Radiation Database (NSRDB) is a serially complete collection
of meteorological and solar irradiance data sets for the United States and a
growing list of international locations for 1998-2017. The NSRDB provides
foundational information to support U.S. Department of Energy programs,
research, and the general public.

The NSRDB provides time-series data at 30 minute resolution of resource
averaged over surface cells of 0.038 degrees in both latitude and longitude,
or nominally 4 km in size. The solar radiation values represent the resource
available to solar energy systems. The data was created using cloud properties
which are generated using the AVHRR Pathfinder Atmospheres-Extended (PATMOS-x)
algorithms developed by the University of Wisconsin. Fast all-sky radiation
model for solar applications (FARMS) in conjunction with the cloud properties,
and aerosol optical depth (AOD) and precipitable water vapor (PWV) from
ancillary source are used to estimate solar irradiance (GHI, DNI, and DHI).
The Global Horizontal Irradiance (GHI) is computed for clear skies using the
REST2 model. For cloud scenes identified by the cloud mask, FARMS is used to
compute GHI. The Direct Normal Irradiance (DNI) for cloud scenes is then
computed using the DISC model. The PATMOS-X model uses half-hourly radiance
images in visible and infrared channels from the GOES series of geostationary
weather satellites.  Ancillary variables needed to run REST2 and FARMS (e.g.,
aerosol optical depth, precipitable water vapor, and albedo) are derived from
the the Modern Era-Retrospective Analysis (MERRA-2) dataset. Temperature and
wind speed data are also derived from MERRA-2 and provided for use in SAM to
compute PV generation.

The following variables are provided by the NSRDB:
- Irradiance:
    - Global Horizontal (ghi)
    - Direct Normal (dni)
    - Diffuse (dhi)
- Clear-sky Irradiance
- Cloud Type
- Dew Point
- Temperature
- Surface Albedo
- Pressure
- Relative Humidity
- Solar Zenith Angle
- Precipitable Water
- Wind Direction
- Wind Speed
- Fill Flag
- Angstrom wavelength exponent (alpha)
- Aerosol optical depth (aod)
- Aerosol asymmetry parameter (asymmetry)
- Cloud optical depth (cld_opd_dcomp)
- Cloud effective radius (cld_ref_dcomp)
- cloud_press_acha
- Reduced ozone vertical pathlength (ozone)
- Aerosol single-scatter albedo (ssa)

## Directory structure

Solar resource data is made available as a series of .h5 files corresponding to
each year and can be found at s3://nrel-pds-nsrdb/hdf5-source-files-v3/nsrdb_${year}.h5

The NSRDB data is also available via HSDS at /nrel/nsrdb/nsrdb_${year}.h5

For examples on setting up and using HSDS please see our [examples repository](https://github.com/nrel/hsds-examples)

## Data Format

The data is provided in high density data file (.h5) separated by year.  The
variables mentioned above are provided in 2 dimensional time-series arrays with
dimensions (time x location). The temporal axis is defined by the `time_index`
dataset, while the positional axis is defined by the `meta` dataset. For
storage efficiency each variable has been scaled and stored as an integer. The
scale-factor is provided in the 'psm_scale-factor' attribute.  The units for
the variable data is also provided as an attribute (`psm_units`).

## Python Examples

Example scripts to extract solar resource data using python are provided below:

The easiest way to access and extract data from the Resource eXtraction tool
[`rex`](https://github.com/nrel/rex)

```python
from rex import NSRDBX

nsrdb_file = '/nrel/nsrdb/nsrdb_2010.h5'
with NSRDBX(nsrdb_file, hsds=True) as f:
    meta = f.meta
    time_index = f.time_index
    dni = f['dni']
```

`rex` also allows easy extraction of the nearest site to a desired (lat, lon)
location:

```python
from rex import NSRDBX

nsrdb_file = '/nrel/nsrdb/nsrdb_2010.h5'
nrel = (39.741931, -105.169891)
with NSRDBX(nsrdb_file, hsds=True) as f:
    nrel_dni = f.get_lat_lon_df('dni', nrel)
```

or to extract all sites in a given region:

```python
from rex import NSRDBX

nsrdb_file = '/nrel/nsrdb/nsrdb_2010.h5'
state='Colorado'
with NSRDBX(nsrdb_file, hsds=True) as f:
    co_dni = f.get_region_df('dni', state, region_col='state')
```

Lastly, `rex` can be used to extract all variables needed to run SAM at a given
location:

```python
from rex import NSRDBX

nsrdb_file = '/nrel/nsrdb/nsrdb_2010.h5'
nrel = (39.741931, -105.169891)
with NSRDBX(nsrdb_file, hsds=True) as f:
    nrel_sam_vars = f.get_SAM_df(nwtc)
```

If you would rather access the NSRDB data directly using h5pyd:

```python
# Extract the average direct normal irradiance (dni)
import h5pyd
import pandas as pd

# Open .h5 file
with h5pyd.File('/nrel/nsrdb/nsrdb_2010.h5', mode='r') as f:
    # Extract meta data and convert from records array to DataFrame
    meta = pd.DataFrame(f['meta'][...])
    # dni dataset
    dni= f['dni']
    # Extract scale factor
    scale_factor = dni.attrs['psm_scale_factor']
    # Extract, average, and un-scale dni
    mean_dni= dni[...].mean(axis=0) / scale_factor

# Add mean windspeed to meta data
meta['Average DNI'] = mean_dni
```

```python
# Extract time-series data for a single site
import h5pyd
import pandas as pd

# Open .h5 file
with h5pyd.File('/nrel/nsrdb/nsrdb_2010.h5', mode='r') as f:
    # Extract time_index and convert to datetime
    # NOTE: time_index is saved as byte-strings and must be decoded
    time_index = pd.to_datetime(f['time_index'][...].astype(str))
    # Initialize DataFrame to store time-series data
    time_series = pd.DataFrame(index=time_index)
    # Extract variables needed to compute generation from SAM:
    for var in ['dni', 'dhi', 'air_temperature', 'wind_speed']:
    	# Get dataset
    	ds = f[var]
    	# Extract scale factor
    	scale_factor = ds.attrs['psm_scale_factor']
    	# Extract site 100 and add to DataFrame
    	time_series[var] = ds[:, 100] / scale_factor
```

## References

For more information about the NSRDB please see the
[website](https://nsrdb.nrel.gov/)
Users of the NSRDB should please cite:
- [Sengupta, M., Y. Xie, A. Lopez, A. Habte, G. Maclaurin, and J. Shelby. 2018. "The National Solar Radiation Data Base (NSRDB)." Renewable and Sustainable Energy Reviews  89 (June): 51-60.](https://www.sciencedirect.com/science/article/pii/S136403211830087X?via%3Dihub)