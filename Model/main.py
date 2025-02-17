import os
import time
import obstacles
import crowd
import imagerendering_output
import weighted_graph as wg
import cv2
import json

MAX_FILES = 3
directory = "/Users/saumya/Desktop/hackedproject/HackED2025/Model/videos"

def wait_for_file(filename, timeout=10):
    """Wait for a file to be created before proceeding."""
    start_time = time.time()
    while not os.path.exists(filename):
        if time.time() - start_time > timeout:
            print(f"Error: {filename} not found after {timeout} seconds.")
            return False
        time.sleep(1)
    return True

def getImage(filepath):
    obstacles.speed_up_video(filepath, "output.mp4", 5)
    crowd.compute_reachability_map("output.mp4")
    obstacles.compute_reachability_map("output.mp4")
    
    if hasattr(imagerendering_output, "main"):
        imagerendering_output.main()  # Ensure that imagerendering_output has a main()

def djikstra(pointFile):
    with open(pointFile, "r", newline="\n") as f:
        data = f.readlines()

    # Convert the first and last lines into (float, float) tuples
    start = data[0].split(",")
    end = data[-1].split(",")
    start = (float(start[0]), float(start[-1].strip()))
    end = (float(end[0]), float(end[-1].strip()))

    image = cv2.imread("final_overlay.jpg")
    if image is None:
        print("Error: final_overlay.jpg not found or unreadable.")
        return None

    path = wg.returnPath(image, start, end)
    dir_path = "/Users/saumya/Desktop/hackedproject/HackED2025/View/public"
    file_path = os.path.join(dir_path, "output2.json")
    path_json = {"points": path}  

    with open(file_path, "w") as write:
        json.dump(path_json, write, indent=4)  # pretty print for readability

    print("Path saved to output.json:", path_json)
    return path

def isNewFileAdded(directory, prev_files):
    """Returns a set of new files and the current set of files."""
    current_files = set(os.listdir(directory))
    new_files = current_files - prev_files
    return new_files, current_files

def enforce_file_limit(directory, max_files=3):
    """
    Checks the files in the directory and removes the oldest files
    if the number exceeds max_files.
    """
    # Build full paths for only files in the directory.
    files = [os.path.join(directory, f) for f in os.listdir(directory)
             if os.path.isfile(os.path.join(directory, f))]
    
    if len(files) > max_files:
        files.sort(key=lambda x: os.path.getctime(x))  # Oldest first
        num_to_remove = len(files) - max_files
        for i in range(num_to_remove):
            try:
                os.remove(files[i])
                print(f"Removed oldest file: {files[i]}")
            except Exception as e:
                print(f"Error removing file {files[i]}: {e}")

def main():
    run = True
    count = 0
    prev_files = set(os.listdir(directory))  # Initial snapshot

    while run:
        if count == 0:
            if prev_files:
                # Process the first file from the initial snapshot.
                first_file = list(prev_files)[0]
                print(f"Processing initial file: {first_file}")
                getImage(os.path.join(directory, first_file))
                djikstra("/Users/saumya/Desktop/hackedproject/HackED2025/Model/reference_points.txt")
            else:
                print("No initial files found in the directory.")
        else:
            new_files, prev_files = isNewFileAdded(directory, prev_files)
            if new_files:  # Only proceed if a new file is detected.
                new_file = list(new_files)[0]
                print(f"New file detected: {new_file}")
                getImage(os.path.join(directory, new_file))
                djikstra("/Users/saumya/Desktop/hackedproject/HackED2025/Model/reference_points.txt")
                
                # Enforce the maximum file count.
                enforce_file_limit(directory, MAX_FILES)
        
        count += 1
        time.sleep(1)  # Slight delay to avoid busy looping

    # Cleanup generated files when done.
    cleanup_files = [
        "output2.jpg", "output.mp4",
        "final_reachability_map_white.png", "final_reachability_map.png"
    ]
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    main()
