import airsim
import time
import os
import math
import numpy as np
from PIL import Image
import threading
import datetime

# === Setup AirSim connection ===
client = airsim.MultirotorClient(ip="192.168.86.48")
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# === Take off ===
client.takeoffAsync().join()
client.hoverAsync().join()
time.sleep(2)

# === Image output directory ===
base_dir = os.path.expanduser("~/Desktop/AirSimImages/")
date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
image_dir = os.path.join(base_dir, date_str)
os.makedirs(image_dir, exist_ok=True)
print(f"Images will be saved to: {image_dir}")


# === Function to save one image ===
def save_image():
    responses = client.simGetImages(
        [airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)]
    )
    if responses:
        response = responses[0]
        img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(response.height, response.width, 3)
        image = Image.fromarray(img_rgb)
        filename = os.path.join(image_dir, f"img_{int(time.time() * 1000)}.png")
        image.save(filename)
        print(f"Saved {filename}")


# === Background thread: Capture images every N seconds ===
capture_interval = 1
stop_capture = False


def image_capture_loop():
    while not stop_capture:
        save_image()
        time.sleep(capture_interval)


# Start image capture thread
capture_thread = threading.Thread(target=image_capture_loop)
capture_thread.start()

# Move along points


def move_to_points(points, velocity):
    for point in points:
        x, y, z = point
        print(f"Moving to ({x}, {y}, {z}) at {velocity} m/s")
        client.moveToPositionAsync(x, y, z, velocity).join()
        client.hoverAsync().join()


points = [(0, 0, -10), (10, 0, -10), (5, -5, -10), (-5, -6, -10)]

# Move to points
move_to_points(points, 3)

# Stop image capture thread
stop_capture = True
capture_thread.join()

client.hoverAsync().join()
print("Flight complete and image capture stopped.")
