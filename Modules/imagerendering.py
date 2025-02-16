import numpy as np
import cv2
import time
from skimage.filters import gaussian
from sklearn.cluster import KMeans

benchmark = False

def color_quantize(image, n_colors=10):
    """ Reduces image colors using K-Means clustering. """
    start_time = time.time()

    arr = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(arr)
    processed_image = kmeans.cluster_centers_[kmeans.labels_].reshape(image.shape).astype(np.uint8)

    if benchmark:
        print(f"Color quantization took {time.time() - start_time:.4f} seconds")

    return processed_image

def gaussian_blur(original, blurStrength = 1):
    start_time = time.time()

    blurred = gaussian(original, sigma=blurStrength)

    end_time = time.time()

    if benchmark:
        print("Gaussian blur took", end_time - start_time, "seconds to run")

    return (blurred * 255).astype('uint8')


def white_to_redpixels(image):
    """ Converts white pixels (255, 255, 255) to red (0, 0, 255). """
    mask = (image == [255, 255, 255]).all(axis=2)
    image[mask] = [0, 0, 255]
    cv2.imwrite("output2.jpg", image)

    print("Modified image saved as output.jpg")
    return image