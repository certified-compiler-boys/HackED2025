import cv2
import numpy as np
import time
from scipy.interpolate import splprep, splev

# Screen size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Given percentage coordinates
points = [
    (64.84375, 98.95833333333333), (63.28125, 96.875), (61.71875, 94.79166666666667),
    (60.15625, 92.70833333333333), (58.59375, 90.625), (57.03125, 88.54166666666667),
    (55.46875, 86.45833333333333), (53.90625, 84.375), (52.34375, 84.375),
    (50.78125, 82.29166666666667), (49.21875, 80.20833333333333), (47.65625, 80.20833333333333),
    (46.09375, 80.20833333333333), (44.53125, 80.20833333333333), (42.96875, 80.20833333333333),
    (41.40625, 80.20833333333333), (39.84375, 80.20833333333333), (38.28125, 80.20833333333333),
    (36.71875, 80.20833333333333), (35.15625, 80.20833333333333), (33.59375, 78.125)
]

# Convert percentage to pixel positions
pixel_points = np.array([(int(x / 100 * SCREEN_WIDTH), int(y / 100 * SCREEN_HEIGHT)) for x, y in points])

# Generate smooth Bézier-like curves using splines
x_vals, y_vals = pixel_points[:, 0], pixel_points[:, 1]
tck, u = splprep([x_vals, y_vals], s=3)  # Smooth the curve
u_fine = np.linspace(0, 1, 200)  # 200 points for smoothness
smooth_points = np.array(splev(u_fine, tck)).T.astype(np.int32)  # Interpolated smooth path

# Create a black background
frame = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8)

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter("output.mp4", fourcc, 30, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to draw a glowing arrow
def draw_arrow(img, start, end, color=(0, 255, 0)):
    cv2.arrowedLine(img, start, end, color, 4, tipLength=0.3, line_type=cv2.LINE_AA)

# Function to add a fading glow effect
def add_glow(img, points, intensity=5):
    overlay = img.copy()
    for i, (x, y) in enumerate(points):
        alpha = max(0, 255 - (len(points) - i) * intensity)  # Older points fade out
        cv2.circle(overlay, (x, y), 6, (0, 255, 0, alpha), -1, cv2.LINE_AA)
    return cv2.addWeighted(overlay, 0.5, img, 0.5, 0)

# Main animation loop
while True:
    frame.fill(0)  # Reset background to black

    # Draw smooth curve
    for i in range(1, len(smooth_points)):
        cv2.line(frame, tuple(smooth_points[i - 1]), tuple(smooth_points[i]), (0, 200, 0), 2, cv2.LINE_AA)

    # Animate arrow along the smooth curve
    for idx in range(1, len(smooth_points)):
        time.sleep(0.01)  # Delay for smooth animation
        frame = add_glow(frame, smooth_points[:idx])  # Add glowing effect

        # Draw animated moving arrow
        draw_arrow(frame, tuple(smooth_points[idx - 1]), tuple(smooth_points[idx]))

        # Display animation and save frame to video
        cv2.imshow("Curvy Arrow Animation ", frame)
        video_writer.write(frame)

        # Stop when 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            video_writer.release()
            cv2.destroyAllWindows()
            print("Animation stopped. Video saved as 'output.mp4'.")
            exit()