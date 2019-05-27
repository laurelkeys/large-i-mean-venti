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
    Normalizes pixel values to [0, 1] and 
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
    return compressed

def plot_3d(normalized_image, show=True, save_fname=None, use_rgb_colors=True):
    '''
    Plots the image's pixels into the 3D space defined by (x, y, z) = (R, G, B)
    Note: the RGB values must be mapped from [0, 255] to [0, 1]
    '''
    r = normalized_image[:, :, 0].flatten()
    g = normalized_image[:, :, 1].flatten()
    b = normalized_image[:, :, 2].flatten()

    fig = plt.figure()
    ax = Axes3D(fig) # fig.add_subplot(111, projection='3d')
    if use_rgb_colors:
        ax.scatter(r, g, b, c=normalized_image.reshape(-1, 3)) # colors each point with it's RGB color value
    else:
        ax.scatter(r, g, b)

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
k_image = cluster(image, n_clusters) # k colors with RGB values normalized to [0, 1] range

fname = path.join(save_path, f"{image_name}{n_clusters}{image_ext}")
img.imsave(fname, k_image)
print(f"Image saved to {fname}")

plot_3d(image / 255) # maps the colors from [0, 255] to [0, 1] for color plotting
plot_3d(k_image)