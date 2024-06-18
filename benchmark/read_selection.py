import h5pyd
import h5py
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

if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
    usage = f"Usage:  {sys.argv[0]} <filepath>\n"
    usage += f"Example: python {sys.argv[0]} hdf5://nrel/nsrdb/conus/nsrdb_conus_2022.h5"
    sys.exit(usage)

filepath = sys.argv[1]

h5path =  "wind_speed"  # change if this dataset is not in the file
bucket = "s3://nrel-pds-hsds"  # bucket for NREL HSDS data, ignored for posix file paths

if filepath.startswith("hdf5://"):
    f = h5pyd.File(filepath, bucket=bucket)
else:
    f = h5py.File(filepath)

print(list(f))

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
