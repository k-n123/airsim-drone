from drone_commands import Drone, lock

drone = Drone("192.168.86.48")

import time
import os
import threading
import datetime


stop_event = threading.Event()


# Image capture function (running in background)
def capture_loop():
    savedir = os.path.expanduser("~/Desktop/AirsimImages/")
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    savedir = os.path.join(savedir, date)
    print("Started image capture loop.")
    while not stop_event.is_set():
        with lock:
            drone.captureImage(save_dir=savedir)
        time.sleep(0.5)
    print("Stopped image capture loop (drone landed).")


# Drone takeoff = initate client
drone.takeoff()

# Start capture loop in background
capture_thread = threading.Thread(target=capture_loop)
capture_thread.start()

# Main thread continues to run commands. Put drone commands here.
try:
    with lock:
        drone.moveTo(20, 20, -20, 3)
        drone.moveTo(-5, -5, -10, 3)

    input("Press Enter to stop capturing images and land the drone...")
finally:
    stop_event.set()
    capture_thread.join()
    with lock:
        drone.land()
    print("Done.")
