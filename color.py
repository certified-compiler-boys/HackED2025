import cv2
import os
import numpy as np

DOESNT_MOVE = (255, 0, 0)  # RED
DOES_MOVE = (255, 255, 255)

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


getFrames("0001-0050.mp4")

def getDifferenceBetween2(framePath1, framePath2):
    frame1 = cv2.imread(framePath1)
    frame2 = cv2.imread(framePath2)

    if frame1 is None or frame2 is None:
        print(f"Error: Could not read frames {framePath1} or {framePath2}")
        return None

    # Convert to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference
    diff = cv2.absdiff(gray1, gray2)

    # Threshold the difference
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    return thresh  # Returning binary difference image
import cv2
import numpy as np

def compute_reachability_map(video_path, subtract_value=50, motion_threshold=30, decay_rate=0):
    """
    Computes a reachability map from a video stream.
    
    The map is initialized as white (255=non-reachable) and gets darkened
    (subtracted) at pixels where motion is detected.
    
    Parameters:
        video_path (str): Path to the video file.
        subtract_value (int): Amount to subtract from each pixel on detecting motion.
        motion_threshold (int): Intensity difference threshold to consider as motion.
        decay_rate (int): Rate to "restore" pixel values back toward white when no motion occurs.
                          Set to 0 to disable.
                          
    Returns:
        reach_map (ndarray): Final reachability map image.
    """
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Error reading video.")
        return None
    
    # Resize for consistency and speed
    frame = cv2.resize(frame, (640, 480))
    gray_prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Initialize the reachability map as white (non-reachable)
    reach_map = np.full(gray_prev.shape, 255, dtype=np.uint8)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Compute the absolute difference between current and previous frames
        diff = cv2.absdiff(gray, gray_prev)
        # Create a binary motion mask based on the threshold
        _, motion_mask = cv2.threshold(diff, motion_threshold, 255, cv2.THRESH_BINARY)
        
        # Subtract from the reachability map where motion is detected
        reach_map = np.where(motion_mask == 255,
                             np.clip(reach_map - subtract_value, 0, 255),
                             reach_map)
        
        # Optional decay: if no motion, gradually restore to white
        if decay_rate > 0:
            reach_map = np.clip(reach_map + decay_rate, 0, 255)
        
        # Optionally display intermediate results (if desired)
        cv2.imshow("Video", frame)
        cv2.imshow("Motion Mask", motion_mask)
        cv2.imshow("Reachability Map", reach_map)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        gray_prev = gray.copy()
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Save the final reachability map as an image file
    cv2.imwrite("final_reachability_map.png", reach_map)
    return reach_map

if __name__ == "__main__":
    video_path = "/Users/saumya/Desktop/model/IMG_8835.mp4"
    final_map = compute_reachability_map(video_path,
                                          subtract_value=50,
                                          motion_threshold=30,
                                          decay_rate=0)
    if final_map is not None:
        # Show the final output image in a window
        cv2.imshow("Final Reachability Map", final_map)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
