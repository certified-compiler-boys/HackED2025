import imagerendering as IMP
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Load first image
pathTest = "testing.jpg"
original = cv2.imread(pathTest)

if original is None:
    print("Error: Could not load testing.jpg. Check the file path.")
    exit()

# Step 1: Apply Gaussian Blur or Color Quantization
processed_image = IMP.gaussian_blur(original, .1)  # Try IMP.color_quantize(original) instead

# Step 2: Convert white pixels to red
final_image = IMP.white_to_redpixels(processed_image)

# Save output image
cv2.imwrite("output2.jpg", final_image)

# Step 3: Overlay output2.jpg onto testing2.jpg
output_img = cv2.imread("output2.jpg")  # Image where white pixels are red
test_img = cv2.imread("testing2.jpg")   # Image that still has white pixels

if test_img is None:
    print("Error: Could not load testing2.jpg. Check the file path.")
    exit()

# Ensure both images have the same dimensions
if output_img.shape != test_img.shape:
    output_img = cv2.resize(output_img, (test_img.shape[1], test_img.shape[0]))

# Create a mask where the pixels in testing2.jpg are white
white_mask = (test_img == [255, 255, 255]).all(axis=2)

# Replace white pixels in testing2.jpg with the corresponding pixels from output2.jpg
test_img[white_mask] = output_img[white_mask]

# Save final overlay image
cv2.imwrite("final_overlay.jpg", test_img)

# Step 4: Display final image
plt.imshow(cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for display
plt.axis("off")
plt.show()

print("Final image saved as final_overlay.jpg")