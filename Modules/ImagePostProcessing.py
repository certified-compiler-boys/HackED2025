import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.filters import gaussian
from sklearn.cluster import KMeans
from skimage import color
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


def gaussian_blur(original, blurStrength = 1):
    start_time = time.time()

    blurred = gaussian(original, sigma=blurStrength)

    end_time = time.time()

    if benchmark:
        print("Gaussian blur took", end_time - start_time, "seconds to run")

    return (blurred * 255).astype('uint8')

def greyscale(original):
    start_time = time.time()

    grayscale_img = color.rgb2gray(original)
    grey_image_rgb = np.stack([grayscale_img] * 3, axis=-1)

    end_time = time.time()

    if benchmark:
        print("Greyscale conversion took", end_time - start_time, "seconds to run")

    grey_image_rgb_uint8 = (grey_image_rgb * 255).astype(np.uint8)

    return grey_image_rgb_uint8  # Returns a 3D RGB grey image
