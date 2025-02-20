import cv2
import numpy as np
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
        # if decay_rate > 0:
        #     reach_map = np.clip(reach_map + decay_rate, 0, 255)
        
        # Optionally display intermediate results (if desired)
        #cv2.imshow("Video", frame)
        #cv2.imshow("Motion Mask", motion_mask)
        #cv2.imshow("Reachability Map", reach_map)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        gray_prev = gray.copy()
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Save the final reachability map as an image file
    #reach_map = cv2.bitwise_not(reach_map)   # COmment out this line if you want reverse color
    cv2.imwrite("final_reachability_map.png", reach_map)
    return reach_map

if __name__ == "__main__":
    video_path = "output.mp4"
    final_map = compute_reachability_map(video_path,
                                          subtract_value=50,
                                          motion_threshold=30,
                                          decay_rate=0)
    if final_map is not None:
        # Show the final output image in a window
        #cv2.imshow("Final Reachability Map", final_map)
        cv2.waitKey(0)
        cv2.destroyAllWindows()