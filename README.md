# NREL Highly Scalable Data Service (HSDS) Examples

NREL's HSDS service provides public access to several of DOEs high-value datasets available internally on the [Kestrel HCP System](https://www.nrel.gov/hpc/kestrel-computing-system.html). Due to the high demand for the HSDS service, **users with access to NREL’s HPC should pursue direct access through that system.**

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
hs_username =
hs_password =
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
- [/nrel/US_wave/](datasets/US_Wave.md)

## Running a Local HSDS Server on EC2 (AWS)
You can stand up a local HSDS server on an EC2 instance to improve the HSDS throughput versus the NREL developer API. Generally you should follow [these instructions](https://github.com/HDFGroup/hsds/blob/master/docs/docker_install_aws.md) from the HSDS documentation. Here are a few tips and tricks to get everything connected to the NREL bucket:

To install docker and docker-compose on an EC2 instance (if not already installed):

1. `sudo amazon-linux-extras install docker`
2. `sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
3. `sudo chmod +x /usr/local/bin/docker-compose`
4. `sudo groupadd docker`
5. `sudo usermod -aG docker $USER`
6. `newgrp docker`
7. `sudo service docker start`
8. `docker run hello-world`

Your ~/.hscfg file should look like this:
```
# local hsds server
hs_endpoint = http://localhost:5101
hs_username = admin
hs_password = admin
hs_api_key = None
hs_bucket = nrel-pds-hsds
```

The following environment variables must be set:
```
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
export BUCKET_NAME=${YOUR_S3_BUCKET_NAME_HERE}
export AWS_REGION=us-west-2
export AWS_S3_GATEWAY=http://s3.us-west-2.amazonaws.com/
export HSDS_ENDPOINT=http://localhost:5101
export LOG_LEVEL=INFO
```

A few miscellaneous tips:

1. You can list the available docker images with `docker images`
2. You can delete the docker HSDS image with `docker rmi $IMAGE_ID` (useful to reset the docker image)
3. If you have AWS permissions issues try using a non-root IAM user with the corresponding AWS credentials as environment variables
4. You can stand up parallel docker HSDS servers by running `sh runall.sh -8 `


## Credit

This software is currently maintained by Reid Olson (reid.olson@nrel.gov). This software was initially developed by Caleb Phillips (caleb.phillips@nrel.gov), John Readey (jreadey@hdfgroup.org), Jordan Perr-Sauer (Jordan.Perr-Sauer@nrel.gov), and Michael Rossol to support the NREL Research Data Initiative and WIND Toolkit at the National Rewnable Energy Laboratory in Golden, Colorado, USA.

## License

Copyright (c) 2017, National Renewable Energy Laboratory (NREL)
All rights reserved. See LICENSE for additional information.
