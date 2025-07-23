from drone_commands import Drone, lock

drone = Drone("192.168.86.48")

import time
import os
import threading
import datetime
import numpy as np


def capture_Images():
    image_dir = os.path.expanduser("~/Desktop/AirsimImages/")
    image_dir += datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "/"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    print(image_dir)

    count = 0
    while not drone.isLanded():
        drone.captureImage(save_dir=image_dir, image_name=str(count) + ".png")
        count += 1
        time.sleep(1)  # capture every second

    print(str(count) + " Images captured")


drone.takeoff()

# Time gap between takeoff and image capture
time.sleep(1)

# Background thread to capture images
image_thread = threading.Thread(target=capture_Images, daemon=True)
image_thread.start()


drone.moveTo(0, 5, -10, 2)
time.sleep(2)

drone.reset()
