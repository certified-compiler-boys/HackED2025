import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from sklearn.cluster import KMeans
import time

benchmark = False

# Posterizes the image and returns it
def color_quantize(original):
    n_colors = 10

    start_time = time.time()
    
    arr = original.reshape((-1, 3))
    kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(arr)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    less_colors = centers[labels].reshape(original.shape).astype('uint8')

    end_time = time.time()

    if benchmark:
        print("My program took", end_time - start_time, "seconds to run")

    return less_colors # PROCESSED STUFF IMAGE

