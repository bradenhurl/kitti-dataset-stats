import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kde
from wavedata.tools.obj_detection import obj_utils
import sys
import os

label_dir = '/object/training/label_2'
output_file = '/media/bradenhurl/hd/bev_heatmap.txt'

dataset_dir = '/home/bradenhurl/GTAData/'
data_dir = dataset_dir + label_dir

startIdx = 0
endIdx = 50000

x = []
y = []
z = []

for idx in range(startIdx,endIdx):
    sys.stdout.write("\rProcessing index {} / {}".format(
        idx + 1 - startIdx, endIdx - startIdx))
    filepath = data_dir + '/' + "{:06d}.txt".format(idx)
    if os.stat(filepath).st_size != 0:
        obj_list = obj_utils.read_labels(data_dir, idx)
        for obj in obj_list:
            if obj.type == 'Pedestrian':
                x.append(obj.t[0])
                y.append(obj.t[1])
                z.append(obj.t[2])

#x/y for this visualization represent right/forward (x/z in kitti cam coords)
x = np.array(x)
y = np.array(z)
data = np.vstack([x,y]).T
 
# Create a figure with 6 plot areas
fig, axes = plt.subplots(ncols=6, nrows=1, figsize=(21, 5))
 
# Everything sarts with a Scatterplot
axes[0].set_title('Scatterplot')
axes[0].plot(x, y, 'ko')
# As you can see there is a lot of overplottin here!
 
# Thus we can cut the plotting window in several hexbins
nbins = 20
axes[1].set_title('Hexbin')
axes[1].hexbin(x, y, gridsize=nbins, cmap=plt.cm.BuGn_r)
 
# 2D Histogram
axes[2].set_title('2D Histogram')
axes[2].hist2d(x, y, bins=nbins, cmap=plt.cm.BuGn_r)
 
# Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
k = kde.gaussian_kde(data.T)
xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))
 
# plot a density
axes[3].set_title('Calculate Gaussian KDE')
axes[3].pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.BuGn_r)
 
# add shading
axes[4].set_title('2D Density with shading')
axes[4].pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gouraud', cmap=plt.cm.BuGn_r)

plt.show()