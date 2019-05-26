from os import path
from sys import argv
from time import time
from skimage import io
from sklearn.cluster import KMeans

import functools
import numpy as np
import matplotlib.image as img

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

try:
    image_fname = argv[1]
    image_name, image_ext = path.splitext(path.split(image_fname)[-1])
    n_clusters = int(argv[2]) if len(argv) > 2 else 128
    save_path = argv[3] if len(argv) > 3 else ""
except:
    print('\nusage: k_means.py image_fname [n_clusters] [save_path]')
    exit()

image = io.imread(image_fname)
image = cluster(image, n_clusters)

fname = path.join(save_path, f"{image_name}{n_clusters}{image_ext}")
img.imsave(fname, image)
print(f"Image saved to `{fname}`")