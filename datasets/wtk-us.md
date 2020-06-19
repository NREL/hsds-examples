# Wind Integration National Dataset (WIND Toolkit) Gridded Data Cube

/nrel/wtk_us.h5

## Data Layout

The data has three dimensions: latitudinal index, longitudinal index, and temporal index and is arranged in a uniform matrix:

![](https://github.com/NREL/hsds-examples/blob/master/bin/docs/cube.png?raw=true)

The coordinates are thus defined:

 * t = number of hours since 12AM on the 1st of January, 2007 UTC. Up to hour 61368, which would be 7 years worth of data.
 * y = index of lambert conic coordinates.
 * x = index of lambert conic coordinates.

*Note: All data are instantaneous in time.*

At any point there exist 37 variables, or datasets:

Datasets (t,x,y)

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

There are two special datasets for indexing and time slicing:

 * coordinates (y,x) - lat/lon coordinates for every point on the x/y grid (original projection is a modified Lambert Conic)
 * datetime (t) - YYYYMMDDHHMMSS datetimestamp for every time in the time dimension


## Units

 * Pressure: Pa
 * Temperature: K
 * Direction: degree
 * Speed: m s-1
 * GHI: W m-2
 * inversemoninobukhovlength_2m: m-1

## Data Access

Use the `h5pyd.File` function to open a connection to the server.

```
f = h5pyd.File("/nrel/wtk-us.h5", 'r')
```

Most datasets can be access with the following pattern:

```
f[dataset][t,y,x]
```

The indices support numpy-style indexing, including slices. For example:

```
f = h5pyd.File("/nrel/wtk-us.h5", 'r')
one_value = f["windspeed_100m"][42,42,42]
timeseries = f["windspeed_100m"][:,42,42]
map = f["windspeed_100m"][42,:,:]
```

Downsampling can also be accomplished easily by using a numpy-style skip parameter:

```
downsampled_map = f["windspeed_100m"][42,::16,::16] # every 16th point
downsampled_timeseries = f["windspeed_100m"][::24,42,42] # daily (every 24 hours)
```

Special datasets may not have three dimensions.

```
#retrieve the latitude and longitude of y=0, x=0.
coordinate = f["coordinates"][0,0]

#retrieve the datetime string for t=0.
datetime = f["datetime"][0]
```