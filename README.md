# NREL Highly Scalable Data Service (HSDS) Examples

NREL's HSDS service provides public access to several of DOEs high-value datasets available internally on the [Eagle HCP System](https://www.nrel.gov/hpc/eagle-datasets.html). Due to the high demand for the HSDS service, **users with access to NREL’s HPC should pursue direct access through that system.**

This repository provides examples and convenience functions for accessing the below datasets using HSDS:
- [Wind Integration National Dataset (WIND) Toolkit](https://www.nrel.gov/grid/wind-toolkit.html)
- [National Solar Radiation Database (NSRDB)](https://nsrdb.nrel.gov/)

This service operates with the HSDS software developed by the [HDF Group](https://www.hdfgroup.org/) and is hosted on Amazon Web Services (AWS) using a combination of EC2 (Elastic Compute) and S3 (Scalable Storage Service). You can read more about the HSDS service [in this slide deck](https://www.slideshare.net/HDFEOS/hdf-cloud-services).

## How to Use

To get started, [download Anaconda](https://anaconda.org/anaconda/python) or another distribution of Python, install the h5pyd library:

```
pip install --user h5pyd
```

Next you'll need to configure HSDS:

```
hsconfigure
```

and enter at the prompt:

```
hs_endpoint = https://developer.nrel.gov/api/hsds
hs_username = None
hs_password = None
hs_api_key = 3K3JQbjZmWctY0xmIfSYvYgtIcM3CN0cb1Y2w9bf
```

**IMPORTANT: The example API key here is for demonstation and is rate-limited per IP. To get your own API key, visit https://developer.nrel.gov/signup/**

You can also add the above contents to a configuration file at ~/.hscfg

Finally, you can use Jupyter Notebook to view the example notebooks:

```
cd notebooks
jupyter notebook
```

## Datasets

- [/nrel/wtk_us.h5](datasets/wtk-us.md)
- [/nrel/wtk/](datasets/WINDToolkit.md)
- [/nrel/wtk-5min/](datasets/WINDToolkit.md)
- [/nrel/nsrdb/](datasets/NSRDB.md)

## Credit

This software is currently developed and maintained by Michael Rossol (michael.rossol@nrel.gov). This software was initially developed by Caleb Phillips (caleb.phillips@nrel.gov), John Readey (jreadey@hdfgroup.org), and Jordan Perr-Sauer (Jordan.Perr-Sauer@nrel.gov) to support the NREL Research Data Initiative and WIND Toolkit at the National Rewnable Energy Laboratory in Golden, Colorado, USA.

## License

Copyright (c) 2017, National Renewable Energy Laboratory (NREL)
All rights reserved. See LICENSE for additional information.
