# ref.: http://dilloncamp.com/projects/kmeans.html and https://buzzrobot.com/@skt7

import cv2
import functools
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt

from os import path
from sys import argv
from time import time
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

def duration(func):
    @functools.wraps(func)
    def wrapper(*args):
        start = time()
        result = func(*args)
        end = time()
        print(f'({func.__name__}) Δt: {end-start:.4f} seconds')
        return result
    return wrapper

@duration
def normalize(image):
    '''
    Normalizes pixel values to [0, 1] range and 
    reshapes from (height, width, 3) to (height * width, 3)
    '''
    return (image / 255).reshape(-1, 3)

@duration
def cluster(image, n_clusters, n_init=10, max_iter=300):
    '''
    Groups the image's pixels into clusters by their color similarity and 
    then creates an image representation using only the n_clusters colors
    '''
    normalized = normalize(image)
    k_colors = KMeans(n_clusters, n_init=n_init, max_iter=max_iter).fit(normalized)
    compressed = k_colors.cluster_centers_[k_colors.labels_]
    compressed = np.reshape(compressed, (image.shape))
    return compressed, k_colors.labels_, k_colors.cluster_centers_

def plot_3d(image, show=True, save_fname=None, use_rgb_colors=True):
    '''
    Plots the image's pixels into the 3D space defined by (x, y, z) = (R, G, B)
    '''
    r = image[:, :, 0].flatten()
    g = image[:, :, 1].flatten()
    b = image[:, :, 2].flatten()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(r, g, b, c=None if not use_rgb_colors
               else image.reshape(-1, 3) / 255) # colors each point with it's RGB color value

    if save_fname: plt.savefig(save_fname)
    if show: plt.show()

def plot_clusters(image, labels, colors, show=True, save_fname=None):
    '''
    Plots the original image's pixels with their cluster colors
    '''
    r = image[:, :, 0].flatten()
    g = image[:, :, 1].flatten()
    b = image[:, :, 2].flatten()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(r, g, b, c=colors[labels] / 255)

    if save_fname: plt.savefig(save_fname)
    if show: plt.show()

def plot_histogram(n_clusters, colors, show=True, save_fname=None):
    '''
    Plots the original image's pixels with their cluster colors
    Note: the RGB values must be mapped from [0, 255] to [0, 1]
    '''
    hist, _ = np.histogram(labels, bins=n_clusters)
    hist = hist.astype("float") / hist.sum()
    
    # order by decreasing color frequency
    colors = colors[(-hist).argsort()]
    hist = hist[(-hist).argsort()]
    
    chart = np.zeros((50, 500, 3), dtype=np.uint8)

    start = 0
    for i in range(n_clusters):
        end = start + hist[i] * 500
        r, g, b = colors[i][0:3]
        cv2.rectangle(img=chart, pt1=(int(start), 0), pt2=(int(end), 50), color=(r, g, b), thickness=-1)
        start = end	
    
    plt.figure()
    plt.axis("off")
    plt.imshow(chart)
    if save_fname: plt.savefig(save_fname)
    if show: plt.show()

try:
    image_fname = argv[1]
    image_name, image_ext = path.splitext(path.split(image_fname)[-1])
    n_clusters = int(argv[2]) if len(argv) > 2 else 128
    save_path = argv[3] if len(argv) > 3 else ""
except:
    print('\nusage: k_means.py image_fname [n_clusters] [save_path]')
    exit()

image = cv2.cvtColor(cv2.imread(image_fname), cv2.COLOR_BGR2RGB)
k_image, labels, cluster_centers = cluster(image, n_clusters) # k colors with RGB values normalized to [0, 1] range

fname = path.join(save_path, f"{image_name}{n_clusters}{image_ext}")
img.imsave(fname, k_image)
print(f"Image saved to {fname}")

# denormalizes values
k_image *= 255
cluster_centers *= 255

plot_3d(image)
plot_3d(k_image)

plot_clusters(image, labels, colors=cluster_centers)

plot_histogram(n_clusters, colors=cluster_centers)