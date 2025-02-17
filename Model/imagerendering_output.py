import imagerendering as IMP
import matplotlib.pyplot as plt
import cv2

# Load first image
def main():
    pathTest = "final_reachability_map.png"
    original = cv2.imread(pathTest)
    
    if original is None:
        print("Error: Could not load final_reachability_map.png. Check the file path.")
        exit()

    # Step 1: Apply Gaussian Blur or Color Quantization
    processed_image = IMP.gaussian_blur(original, 0.1)  # Try IMP.color_quantize(original) instead

    # Step 2: Convert white pixels to red
    final_image = IMP.white_to_redpixels(processed_image)

    # Step 3: Overlay output2.jpg onto final_reachability_map_white.png
    overlayed_image = IMP.overlay_images("output2.jpg", "final_reachability_map_white.png")

    # Step 4: Display final image
    if overlayed_image is not None:
        plt.imshow(cv2.cvtColor(overlayed_image, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for display
        plt.axis("off")
        # plt.show()

if __name__ == "__main__":
    main()