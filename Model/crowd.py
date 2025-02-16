import cv2
import os
import numpy as np

DOESNT_MOVE = (255, 255, 255)  # WHITE
DOES_MOVE = (0, 0, 0)  # BLACK

def compute_reachability_map(video_path, subtract_value=5, motion_threshold=30):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    if not ret:
        print("Error reading video.")
        return None

    frame = cv2.resize(frame, (640, 480))
    gray_prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Initialize reachability map as White (255,255,255 in BGR)
    height, width = gray_prev.shape
    reach_map = np.full((height, width, 3), 255, dtype=np.uint8)  # White background
    cap = cv2.VideoCapture("output.mp4")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute absolute difference for motion detection
        diff = cv2.absdiff(gray, gray_prev)
        _, motion_mask = cv2.threshold(diff, motion_threshold, 255, cv2.THRESH_BINARY)

        # Darken all color channels equally where motion is detected (fade to black)
        reach_map = np.where(
            motion_mask[:, :, None] == 255,  # Apply condition to all channels
            np.clip(reach_map - subtract_value, 0, 255),  # Reduce brightness
            reach_map
        )

        # Display the reachability map
        #cv2.imshow("Reachability Map (White Background)", reach_map)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        gray_prev = gray.copy()

    cap.release()
    cv2.destroyAllWindows()

    # Save the final reachability map
    cv2.imwrite("final_reachability_map_white.png", reach_map)
    #reach_map = cv2.bitwise_not(reach_map)
    return reach_map

# Run the function
if __name__ == "__main__":
    video_path = "dice_original.mp4"
    final_map = compute_reachability_map(video_path, subtract_value=5, motion_threshold=30)
    #cv2.imshow("Final Reachability Map", final_map)
    cv2.waitKey(0)
    cv2.destroyAllWindows()