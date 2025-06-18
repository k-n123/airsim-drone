#Import modules 

import setup_path
import airsim

import numpy as np
import time
import os
import tempfile
import pprint
import cv2
import keyboard


'''
Before running, open AirSim binary or unreal engine project and press play (have simulator running)
'''

#Setup Airsim client 

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)


# the following funcitons will get the state/data of certain aspects and return their states 

def getDroneState():
    state = client.getMultirotorState()
    s = pprint.pformat(state)
    print("state: %s" % s)

def getImuData():
    imu_data = client.getImuData()
    s = pprint.pformat(imu_data)
    print("imu_data: %s" % s)

def getBarometerData():
    barometer_data = client.getBarometerData()
    s = pprint.pformat(barometer_data)
    print("barometer_data: %s" % s)

def getMagnetometerData():
    magnetometer_data = client.getMagnetometerData()
    s = pprint.pformat(magnetometer_data)
    print("magnetometer_data: %s" % s)

def getGPSData():
    gps_data = client.getGpsData()
    s = pprint.pformat(gps_data)
    print("gps_data: %s" % s)

# getCoordinates() returns the location of the drone as a tuple
def getCoordinates():
    state = client.getMultirotorState()
    position = state.kinematics_estimated.position
    x = position.x_val
    y = position.y_val
    z = position.z_val
    return (x, y, z)

# takeoff() will wait for the user to press a key before arming the drone and asynchronously taking off

def takeoff():
    airsim.wait_key('Press any key to takeoff')
    print("Taking off...")
    client.armDisarm(True)
    client.takeoffAsync().join()

# moveTo() will move the drone to the given x, y, z coordinate at given speed (s) meters/second

def moveTo(x, y, z, s):
    airsim.wait_key(f"Press any key to move vehicle to ({x}, {y}, {z}) at {s} m/s")
    client.moveToPositionAsync(x, y, z, s).join()

# land() will land the drone, disarm it, and disable api control

def land():
    airsim.wait_key("Press any key to land vehicle")
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)


# reset() will reset the client to where it started and disable api control

def reset():
    airsim.wait_key('Press any key to reset to original state')

    client.reset()
    client.armDisarm(False)

    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)





def capture_and_save_image(image_type=airsim.ImageType.Scene, camera_name="0", vehicle_name="", save_dir="images", image_name=None):
    """
    Captures an image from the drone's camera and saves it to the specified directory.

    Parameters:
        client (airsim.MultirotorClient): An active AirSim client.
        image_type (airsim.ImageType): Type of image to capture (Scene, Depth, Segmentation, etc.).
        camera_name (str): Camera name, usually "0" for the default front camera.
        vehicle_name (str): Vehicle name if multiple drones are used.
        save_dir (str): Directory to save the image.
        image_name (str): Custom filename; if None, uses timestamp.
    """
    airsim.wait_key("Press any key to capture image")

    #save_dir = "\Users\renta\OneDrive\Documents\Images"
    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Capture image
    response = client.simGetImage(camera_name, image_type, vehicle_name=vehicle_name)

    
    if response is None:
        print("Failed to get image from AirSim.")
        return None

    # Convert the image bytes to NumPy array
    img1d = np.frombuffer(response, dtype=np.uint8)
    img_rgb = cv2.imdecode(img1d, cv2.IMREAD_UNCHANGED)

    if img_rgb is None:
        print("Image decode failed.")
        return None

    # Generate image filename
    if image_name is None:
        timestamp = int(time.time() * 1000)
        image_name = f"image_{timestamp}.png"

    save_path = os.path.join(save_dir, image_name)

    # Save using OpenCV
    cv2.imwrite(save_path, img_rgb)
    print(f"Image saved to: {save_path}")

    return save_path


getDroneState()
takeoff()
moveTo(-10, 20, -10, 5)
print(getCoordinates())
capture_and_save_image(save_dir="C:/Users/renta/OneDrive/Documents/Images")
getDroneState()
reset()

