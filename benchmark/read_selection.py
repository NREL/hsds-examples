import h5pyd
import h5py
import s3fs
import random
import sys
import time


def get_indices(extent, count):
    indices = set()
    while len(indices) < count:
        index = random.randint(0, extent-1)
        indices.add(index)
    indices = list(indices)
    indices.sort()
    return indices 

#
# main
#

usage = f"Usage:  {sys.argv[0]} [s3fs | hsds]"

if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
    sys.exit(usage)

h5path =  "wind_speed"  # change if this dataset is not in the file

if len(sys.argv) > 1:
    if sys.argv[1] not in ("s3fs", "hsds"):
        sys.exit(usage)
    driver = sys.argv[1]
else:
    driver = "hsds"  # default to hsds

if driver == "s3fs":
    # s3fs enables h5py to "see" S3 files as read-only posix files
    s3_uri = "s3://nrel-pds-nsrdb/conus/nsrdb_conus_pv_2022.h5"
    s3 = s3fs.S3FileSystem(anon=True)
    print(f"opening HDF5 file at: {s3_uri} with s3fs")
    f = h5py.File(s3.open("s3://nrel-pds-nsrdb/conus/nsrdb_conus_pv_2022.h5", "rb"), "r")
else:
    hsds_domain = "hdf5://nrel/nsrdb/conus/nsrdb_conus_2022.h5"
    hsds_bucket = "s3://nrel-pds-hsds"  # bucket for NREL HSDS data
    print(f"opening HSDS domain: {hsds_domain} on bucket: {hsds_bucket}")
    f = h5pyd.File(hsds_domain, bucket=hsds_bucket)

if h5path not in f:
    sys.exit(f"{h5path} dataset not found")

dset = f[h5path]
print(f"{h5path}: {dset}")
print(f"chunks: {dset.chunks}")
print(f"compression: {dset.compression}")

# read x-y slices 

indices = get_indices(dset.shape[1], 10)

for index in indices:
    t = time.time()
    arr = dset[:, index]
    elapsed = time.time() - t
    print(f"dset[:, {index:8n}] min: {arr.min():8.2f} max: {arr.max():8.2f} mean: {arr.mean():8.2f} ({elapsed:.2f} s)")

f.close()
