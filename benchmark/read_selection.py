import h5pyd
import h5py
import random
import sys
import logging

def get_indices(extent, count, fixed=False):
    indices = []
    for i in range(count):
        if fixed:
            if i==0:
                index = 0
            else:
                index = indices[i-1] + (extent // count)
        else:
            index = random.randint(0, extent-1)
        indices.append(index)
    indices.sort()
    return indices 
    

#
# main
#

if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
    msg = f"Usage:  {sys.argv[0]} [--fixed] <filepath> [h5path]\n"
    msg += f"Example: python {sys.argv[0]} hdf5://nrel/nsrdb/conus/nsrdb_conus_2022.h5"
    sys.exit(msg)

arg_num = 1

if sys.argv[arg_num] == "--fixed":
    fixed = True
    arg_num += 1
else:
    fixed = False

filepath = sys.argv[arg_num]
arg_num += 1

if len(sys.argv) > arg_num:
    h5path = sys.argv[arg_num]
else:
    h5path =  "air_temperature"

print(f"filepath: {filepath}")
print(f"h5path: {h5path}")

loglevel = logging.DEBUG
logging.basicConfig(format='%(asctime)s %(message)s', level=loglevel)

if filepath.startswith("hdf5://"):
    f = h5pyd.File(filepath, bucket="nrel-pds-hsds")
else:
    f = h5py.File(filepath)

if h5path not in f:
    sys.exit(f"{h5path} not found, use 'hsls {filepath}' to see all h5paths")

dset = f[h5path]

print(f"shape: {dset.shape}")
print(f"chunks: {dset.chunks}")
print(f"compression: {dset.compression}")

rank = len(dset.shape)
if rank != 2:
    sys.exit(f"{h5path} has rank {rank}, this example only works with two-dimensional datasets")

# read x-y slices 

indices = get_indices(dset.shape[0], 10, fixed=fixed)
print(f"indices: {indices}")

for index in indices:
    arr = dset[index, :]
    print(f"dset[{index},:] min: {arr.min():.2f} max: {arr.max():.2f} mean: {arr.mean():.2f}")

f.close()
