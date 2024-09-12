import h5pyd
import h5py
import os
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

usage = f"Usage:  {sys.argv[0]} [filepath] [h5path]"

if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    print(usage)
    print("filepath prefix:")
    print("   hdf5:// -- use HSDS")
    print("   s3fs:// -- use s3fs")
    print("   http:// -- use ros3")
    print("else - use local posix with HDF5 lib")
    print("")
    print(f"example: python {sys.argv[0]} hdf5://nrel/nsrdb/conus/nsrdb_conus_2020.h5")
    print(f"example: python {sys.argv[0]} s3://nrel-pds-nsrdb/conus/nsrdb_conus_pv_2020.h5")
    # s3://nrel-pds-nsrdb/v3/nsrdb_2020.h5
    sys.exit(1)

filepath = sys.argv[1]
if filepath.startswith("hdf5://"):
    driver = "hsds"
elif filepath.startswith("s3://"):
    driver = "s3fs"
elif filepath.startswith("http://"):
    driver = "ros3"
else:
    driver = "posix"

if len(sys.argv) > 2:
    h5path = sys.argv[2]
else:
    h5path =  "wind_speed"  # default

if driver == "s3fs":

    try:
        import s3fs
    except ImportError:
        sys.exit("run 'pip install s3fs' to use the s3fs option")
    if not filepath.startswith("s3://"):
        sys.exit("expected filepath to start with 's3://'")
    # s3fs enables h5py to "see" S3 files as read-only posix files
    s3 = s3fs.S3FileSystem(anon=True)
    print(f"opening HDF5 file at: {filepath} with s3fs")
    f = h5py.File(s3.open(filepath, "rb"), "r")
elif driver == "ros3":
    print(f"opening HDF5 file at: {filepath} with ros3")
    f = h5py.File(filepath, driver="ros3")
elif driver == "hsds":
    print(f"opening HSDS domain: {filepath}")
    if "BUCKET_NAME" in os.environ:
        bucket = os.environ["BUCKET_NAME"]
    else:
        bucket = None
    f = h5pyd.File(filepath, bucket=bucket)
else:
    print(f"opening HDF5 file at: {filepath} with hdf5 lib")
    f = h5py.File(filepath)


if h5path not in f:
    sys.exit(f"{h5path} dataset not found")

dset = f[h5path]
print(f"{h5path}: {dset}")
print(f"chunks: {dset.chunks}")
print(f"compression: {dset.compression}")
if isinstance(dset.id.id, str):
    # hsds
    layout = dset.id.dcpl_json["layout"]
    s3_uri = layout["file_uri"]
    print(f"links to: {s3_uri}")

# read x-y slices 

indices = get_indices(dset.shape[1], 10)

total_time = 0.0
for index in indices:
    t = time.time()
    arr = dset[:, index]
    elapsed = time.time() - t
    print(f"dset[:, {index:8n}] min: {arr.min():8.2f} max: {arr.max():8.2f} mean: {arr.mean():8.2f} ({elapsed:.2f} s)")
    total_time += elapsed
f.close()
avg_elapsed = total_time / len(indices)
print(f"avg time: {avg_elapsed:.2f} s")
