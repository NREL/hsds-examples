## NREL Wind Toolkit Scalable Data Service Examples

This repository provides examples and convenience functions for working with the National Renewable Energy Laboratory (NREL) Wind Integration National Dataset (WIND) Toolkit Scalable Data Service (SDS).

The WIND Toolkit SDS operates using the HSDS software developed by the [HDF Group](https://www.hdfgroup.org/) and is hosted on Amazon Web Services (AWS) using a combination of EC2 (Elastic Compute) and S3 (Scalable Storage Service). You can read more about the HSDS service [in this slide deck](https://www.slideshare.net/HDFEOS/hdf-cloud-services).

### How to Use

To get started, [download Anaconda](https://anaconda.org/anaconda/python) or another distribution of Python, install the h5pyd library:

```
pip install --user git+http://github.com/HDFGroup/h5pyd.git
```

Then, you can make a configuration file at ~/.hscfg with contents like so:

```
hs_endpoint = https://developer.nrel.gov/api/hsds/
hs_username = None
hs_password = None
hs_api_key = 3K3JQbjZmWctY0xmIfSYvYgtIcM3CN0cb1Y2w9bf
```

*The example API key here is for demonstation and is rate-limited per IP. To get your own API key, visit https://developer.nrel.gov/signup/*

Finally, you can use Jupyter Notebook to view the example notebooks:

```
cd notebooks
jupyter notebook
```
### Data Layout

The data has three dimensions: latitudinal index, longitudinal index, and temporal index and is arranged in a uniform matrix:

![](https://github.com/NREL/hsds-examples/blob/develop/docs/cube.png)

At any point, there are 37 variables:

 * DIF
 * DNI
 * GHI
 * inversemoninobukhovlength_2m
 * precipitationrate_0m
 * pressure_0m
 * pressure_100m
 * pressure_200m
 * relativehumidity_2m
 * temperature_100m
 * temperature_10m
 * temperature_120m
 * temperature_140m
 * temperature_160m
 * temperature_200m
 * temperature_2m
 * temperature_40m
 * temperature_60
 * temperature_80m
 * winddirection_100m
 * winddirection_10m
 * winddirection_120m
 * winddirection_140m
 * winddirection_160m
 * winddirection_200m
 * winddirection_40m
 * winddirection_60m
 * winddirection_80m
 * windspeed_100m
 * windspeed_10m
 * windspeed_120m
 * windspeed_140m
 * windspeed_160m
 * windspeed_200m
 * windspeed_40m
 * windspeed_60m
 * windspeed_80m

To access a subset of data, numpy indexing can be used:

```
f = h5pyd.File("/nrel/wtk-us.h5", 'r')  
one_value = f["windspeed_100m"][42,42,42]
timeseries = f["windspeed_100m"][:,42,42]
map = f["windspeed_100m"][42,:,:]
```

Downsampling can also be accomplished easily:

```
downsampled_map = f["windspeed_100m"][42,::16,::16] # every 16th point
downsampled_timeseries = f["windspeed_100m"][::24,42,42] # daily (every 24 hours)
```

There are two special datasets for indexing and time slicing:

  * coordinates - lat/lon coordinates for every point on the x/y grid (original projection is a modified Lambert Conic)
  * datetime - YYYYMMDDHHMMSS datetimestamp for every time in the time dimension

### Credit

This software was developed by Caleb Phillips (caleb.phillips@nrel.gov), John Readey (jreadey@hdfgroup.org), and Jordan Perr-Sauer (Jordan.Perr-Sauer@nrel.gov) to support the NREL Research Data Initiative and WIND Toolkit at the National Rewnable Energy Laboratory in Golden, Colorado, USA.

### License

Copyright (c) 2017, National Renewable Energy Laboratory (NREL)
All rights reserved. See LICENSE for additional information.