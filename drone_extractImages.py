import time
import os
import threading
import datetime
from drone_commands import Drone

drone = Drone("192.168.86.48")


def capture_images():
    image_dir = os.path.expanduser("~/Desktop/AirsimImages/")
    image_dir += datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "/"
    os.makedirs(image_dir, exist_ok=True)
    print("Saving images to:", image_dir)

    while drone.isLanded():
        time.sleep(0.1)

    count = 0
    while not drone.isLanded():
        drone.captureImage(save_dir=image_dir, image_name=f"{count}.png")
        print(f"Captured image {count}.png")
        count += 1
        time.sleep(1)

    print(f"{count} Images captured.")


# Take off first
drone.takeoff()

# Start image capture thread
image_thread = threading.Thread(target=capture_images, daemon=True)
image_thread.start()

drone.moveTo(0, 5, -10, 2)
time.sleep(2)

drone.reset()
