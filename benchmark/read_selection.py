import h5pyd
import h5py
import random
import sys

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
    sys.exit(f"Usage:  {sys.argv[0]} [--fixed] <filepath>")

if sys.argv[1] == "--fixed":
    fixed = True
    filepath = sys.argv[2]
else: 
    fixed = False
    filepath = sys.argv[1]

h5path =  "windspeed_80m"

print(f"filepath: {filepath}")

if filepath.startswith("hdf5://"):
    f = h5pyd.File(filepath)
else:
    f = h5py.File(filepath)

dset = f[h5path]
print(f"{h5path}: {dset}")
print(f"chunks: {dset.chunks}")
print(f"compression: {dset.compression}")

# read x-y slices 

indices = get_indices(dset.shape[0], 10, fixed=fixed)
print(indices)

for index in indices:
    arr = dset[index, :, :]
    print(f"dset[{index},:,:] min: {arr.min():.2f} max: {arr.max():.2f} mean: {arr.mean():.2f}")

f.close()
