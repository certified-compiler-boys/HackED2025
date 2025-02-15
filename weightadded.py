import cv2
import numpy as np

# Load the image
image = cv2.imread('frame1.png')

if image is None:
    raise FileNotFoundError("The image 'fram1.png could not be found")

height, width, _ = image.shape

block_size = 10

average_weights = []

for y in range(0, height, block_size):
    row_weight = []
    for x in range(0, width, block_size):

        block = image[y:y+block_size, x: x+block_size]

        green_channel = block[:,:,1]

        avg_weight = np.mean(green_channel)

        normalized_weight = round(avg_weight / 255.0, 2)

        row_weight.append(normalized_weight)

average_weights.append(row_weight)

for row in average_weights:
    print(row,"\n")
