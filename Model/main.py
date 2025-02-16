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


#TODO VEry important to speed up
obstacles.speed_up_video("dice_original.mp4","output.mp4",5)


# start = time.time()
# Step 1: Run crowd.py
# # before  = time.time()
crowd.compute_reachability_map("output.mp4")
# # print(time.time() - before)
# # before  = time.time()
if not wait_for_file("final_reachability_map.png"):
    exit()
# # print(time.time() - before)

# Step 2: Run obstacles.py
# Ensure final_reachability_map.png is created before proceeding
print("Running obstacles.py to generate final_reachability_map.png...")
obstacles.compute_reachability_map("output.mp4")
# # before  = time.time()
print("Running crowd.py to generate final_reachability_map_white.png...")

# Ensure final_reachability_map_white.png is created before proceeding
# # before  = time.time()
if not wait_for_file("final_reachability_map_white.png"):
    exit()
# # print(time.time() - before)

# Step 3: Run imagerendering_output.py
# # before  = time.time()
print("Running imagerendering_output.py for final processing...")
if hasattr(imagerendering_output, "main"):
    imagerendering_output.main()  # Make sure `main()` exists in imagerendering_output.py
else:
    print("Error: `imagerendering_output.py` does not have a `main()` function.")

# # print(time.time() - before)

print("✅ Processing complete! The final image should be generated, in ."+str(time.time()-start))