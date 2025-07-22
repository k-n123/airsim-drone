
from drone_commands import Drone
drone = Drone("192.168.86.48")

import time
import threading
import datetime

# Drone takeoff = initate client
drone.takeoff()

# Image capture function (running in background)
def capture_loop():
    savedir = "/home/krishnachnani/Desktop/AirsimImages/"
    date = datetime.now()
    savedir = savedir + str(date)
    print("Started image capture loop.")
    while not drone.isLanded():
        drone.captureImage(save_dir=savedir)
        time.sleep(0.5)
    print("Stopped image capture loop (drone landed).")


# Start capture loop in background
capture_thread = threading.Thread(target=capture_loop)
capture_thread.start()

# Main thread continues to run commands. Put drone commands here.

drone.moveTo(20, 20, -20, 3)
drone.moveTo(-5, -5, -10, 3)

drone.land()

# Wait for drone to land manually or in another command
print("Main thread done. Waiting for capture thread to finish if needed...")
capture_thread.join()
