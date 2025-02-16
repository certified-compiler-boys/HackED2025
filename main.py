import os
import time
import obstacles
import crowd
import imagerendering_output

def wait_for_file(filename, timeout=10):
    """Waits for a file to be created before proceeding."""
    start_time = time.time()
    while not os.path.exists(filename):
        if time.time() - start_time > timeout:
            print(f"Error: {filename} not found after {timeout} seconds.")
            return False
        time.sleep(1)
    return True

# Step 1: Run obstacles.py
print("Running obstacles.py to generate final_reachability_map.png...")
obstacles.compute_reachability_map("dice_original.mp4")

# Ensure final_reachability_map.png is created before proceeding
if not wait_for_file("final_reachability_map.png"):
    exit()

# Step 2: Run crowd.py
print("Running crowd.py to generate final_reachability_map_white.png...")
crowd.compute_reachability_map("dice_original.mp4")

# Ensure final_reachability_map_white.png is created before proceeding
if not wait_for_file("final_reachability_map_white.png"):
    exit()

# Step 3: Run imagerendering_output.py
print("Running imagerendering_output.py for final processing...")
if hasattr(imagerendering_output, "main"):
    imagerendering_output.main()  # Make sure `main()` exists in imagerendering_output.py
else:
    print("Error: `imagerendering_output.py` does not have a `main()` function.")

print("✅ Processing complete! The final image should be generated.")