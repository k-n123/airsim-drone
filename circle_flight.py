import airsim
import time
import os
import math
import numpy as np
from PIL import Image
import threading

# === Setup AirSim connection ===
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# === Take off ===
client.takeoffAsync().join()
client.hoverAsync().join()
print("Drone took off and is hovering.")

# === Image output directory ===
image_dir = "airsim_continuous_images"
os.makedirs(image_dir, exist_ok=True)


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
capture_interval = 1  # seconds
stop_capture = False


def image_capture_loop():
    while not stop_capture:
        save_image()
        time.sleep(capture_interval)


# Start image capture thread
capture_thread = threading.Thread(target=image_capture_loop)
capture_thread.start()

# === Circular path ===
radius = 10
z = -5
steps = 36
velocity = 5

# Generate full circular path
path = []
for i in range(steps):
    angle = 2 * math.pi * i / steps
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    path.append(airsim.Vector3r(x, y, z))

print("Starting smooth circular flight while capturing images...")

# Fly along the circular path
client.moveOnPathAsync(
    path,
    velocity,
    drivetrain=airsim.DrivetrainType.ForwardOnly,
    yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0),
    lookahead=-1,
    adaptive_lookahead=1,
).join()

# Stop image capture thread
stop_capture = True
capture_thread.join()

client.hoverAsync().join()
print("Flight complete and image capture stopped.")
