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

def gaussian_blur(original, blurStrength=1):
    """ Applies Gaussian blur to the image. """
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

    print("Modified image saved as output2.jpg")
    return image

def overlay_images(output_img_path, test_img_path, final_output_path="final_overlay.jpg"):
    """ Overlays output_img onto test_img, replacing white pixels in test_img. """
    
    output_img = cv2.imread(output_img_path)  # Image where white pixels are red
    test_img = cv2.imread(test_img_path)  # Image that still has white pixels

    if test_img is None or output_img is None:
        print("Error: Could not load one or both images. Check the file paths.")
        return None

    # Ensure both images have the same dimensions
    if output_img.shape != test_img.shape:
        output_img = cv2.resize(output_img, (test_img.shape[1], test_img.shape[0]))

    # Create a mask where the pixels in test_img are white
    white_mask = (test_img == [255, 255, 255]).all(axis=2)

    # Replace white pixels in test_img with the corresponding pixels from output_img
    test_img[white_mask] = output_img[white_mask]

    # Save final overlay image
    cv2.imwrite(final_output_path, test_img)

    print(f"Final image saved as {final_output_path}")
    return test_img