[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/nrel/hsds-examples)


# NREL Highly Scalable Data Service (HSDS) Examples

NREL has many several of DOE's high-value datasets publicly available on AWS's Simple Storage Service (S3).  While users are free to
download or directly read these files, their large sizes (typically 10's of TBs per file) can make this impractable.  To provide an 
efficient way to access large HDF5 files in the cloud, The HDF Group (https://www.hdfgroup.org) has developed a REST-based data service 
known as HSDS (Highly Scalable Data Service).  HSDS provides high performance access to these files via the use of parallel processing to 
obtain the highest bandwidth possible from S3.  You can read more about the HSDS service here: https://www.hdfgroup.org/solutions/highly-scalable-data-service-hsds/.  


This repository provides examples and convenience functions for accessing the below datasets using HSDS:
- [Wind Integration National Dataset (WIND) Toolkit](https://www.nrel.gov/grid/wind-toolkit.html)
- [National Solar Radiation Database (NSRDB)](https://nsrdb.nrel.gov/)


## How to Use

here are several options for using HSDS to access NREL datasets.  The most common approaches are:

1. Use GitHub Codespaces
2. Access the NREL developer API
3. Setup a local HSDS server on EC2 (AWS)

Options 1 or 2 are the two easiest ways to get started.  Option 3 requires an AWS account and will incur AWS charges for every hour the
EC2 instance is running, but this option may be best suited for users planning long-running, heavy access to NREL datasets.

Setup instructions for each appoach follow.

### Use GitHub Codespaces

GitHub Codespaces are a convienent way to run your development environment in the cloud.  This repository includes the necessary
configuration files to run as a CodeSpace, no additional software is required.  When the codespace is launched, HSDS will be running
in the background as part of the codespace.  And since the codespace runs in the cloud, access to the NREL data on S3 is quite fast. 
To learn more about CodeSpaces, see: https://docs.github.com/en/codespaces/overview.  

Github provides 120 free core hours (equivalent to running this repository continuously for 30 hours) per  account per month.
For details on pricing, see: https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces.

Running this repository as codespace:

1. Open: https://github.com/codespaces  (or just click on the codespace banner at the top of this page)
2. If you are not signed in to GitHub, sign in
3. Click the "New codespace" button
4. On the next page select the "NREL/hsds-examples" repository
5. Select "US West" as the region
6. Click the "Create Codespace" button

It will take a few minutes until your codespace is ready to use.  Once ready, you can run any of the notebooks in this repository.

When running the first cell in a notebook, you will be prompted to select a "kernel".  To do so, choose "Python Environments" and
then "Python 3.10.13".

Once your work is complete, you can delete the codespace, by going to http://github.com/codespaces, selecting our codespace, and clicking the "delete" button.

### Access the NREL developer API

The second mehtod is to access the NREL developer API.  This is a web API that can be used to connect to an HSDS instances hosted by NREL.
Since it is a shared resource, performance may be impacted by the number of other users accessing the API at any given time.


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


## Datasets

- [/nrel/wtk_us.h5](datasets/wtk-us.md)
- [/nrel/wtk/](datasets/WINDToolkit.md)
- [/nrel/wtk-5min/](datasets/WINDToolkit.md)
- [/nrel/nsrdb/](datasets/NSRDB.md)
- [/nrel/US_wave/](datasets/US_Wave.md)

## Credit

This software is currently maintained by Reid Olson (reid.olson@nrel.gov). This software was initially developed by Caleb Phillips (caleb.phillips@nrel.gov), John Readey (jreadey@hdfgroup.org), Jordan Perr-Sauer (Jordan.Perr-Sauer@nrel.gov), and Michael Rossol to support the NREL Research Data Initiative and WIND Toolkit at the National Rewnable Energy Laboratory in Golden, Colorado, USA.

## License

Copyright (c) 2017, National Renewable Energy Laboratory (NREL)
All rights reserved. See LICENSE for additional information.
