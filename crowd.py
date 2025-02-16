import cv2
import os
import numpy as np

DOESNT_MOVE = (255, 255, 255)  # WHITE
DOES_MOVE = (0, 0, 0)  # BLACK

def getFrames(filepath):
    videoSrc = cv2.VideoCapture(filepath)

    if not videoSrc.isOpened():
        print("Error: Could not open video file.")
    else:
        output_folder = "frames"
        os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

        frameCounter = 0
        success, image = videoSrc.read()

        while success:
            filename = os.path.join(output_folder, f"imageFrame{frameCounter}.jpg")
            cv2.imwrite(filename, image)

            frameCounter += 1
            success, image = videoSrc.read()

        videoSrc.release()  # Release the video capture
        print(f"Extracted {frameCounter} frames successfully.")
def speed_up_video(input_video_path, output_video_path, speed_factor=2):
    cap = cv2.VideoCapture(input_video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps * speed_factor, (width, height))

    frame_index = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index % speed_factor == 0:
            out.write(frame)
        frame_index += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()
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
    speed_up_video(video_path,"output.mp4",4)
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
        cv2.imshow("Reachability Map (White Background)", reach_map)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        gray_prev = gray.copy()

    cap.release()
    cv2.destroyAllWindows()

    # Save the final reachability map
    cv2.imwrite("final_reachability_map_white.png", reach_map)
    reach_map = cv2.bitwise_not(reach_map)
    return reach_map

# Run the function
if __name__ == "__main__":
    video_path = "example2.mp4"
    final_map = compute_reachability_map(video_path, subtract_value=5, motion_threshold=30)
    cv2.imshow("Final Reachability Map", final_map)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
