# Import modules

import setup_path
import airsim

import numpy as np
import time
import os
import tempfile
import pprint
import cv2
import threading
import asyncio

lock = threading.Lock()


"""
Before running, open AirSim binary or unreal engine project and press play (have simulator running)
"""

"""

class Drone(): initalizes an Airsim drone and enables API control

Contains the following functions:
    getDroneState(): prints state of drone
    getImuData(): prints IMU data
    getBarometerData(): prints barometer data
    getMagnetometerData(): prints magnetometer data
    getGpsData(): prints GPS data

    getCoordinates(): returns a tuple of the drone's NED coordinates as (x, y, z)

    takeoff(): arms drone and runs takeoff sequence
    land(): lands drone, disarms drone, and disables API control
    reset(): resets drone to original starting position, disarms drone, and disables API control

    moveTo(x, y, z, s): moves drone to (x, y, z) coordinates at s meters/second
    moveForward(): moves drone forward 5 meters at 5 meters/second
    moveBackward(): moves drone backward 5 meters at 5 meters/second
    moveLeft(): moves drone left 5 meters at 5 meters/second
    moveRight(): moves drone right 5 meters at 5 meters/second

    captureImage(): captures a single image from drone and saves to a given directory
    startRecording(): begins built-in recording API
    stopRecording(): stops recording; saves to /airsim/TIMESTAMP

    setFog(p): sets fog to p percent

"""


class Drone:

    # Setup Airsim client

    def __init__(self, ip_add):
        self.client = airsim.MultirotorClient(ip=ip_add, port=41451)
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    # the following funcitons will get the state/data of certain aspects and return their states

    def getDroneState(self):
        state = self.client.getMultirotorState()
        s = pprint.pformat(state)
        print("state: %s" % s)

    def getImuData(self):
        imu_data = self.client.getImuData()
        s = pprint.pformat(imu_data)
        print("imu_data: %s" % s)

    def getBarometerData(self):
        barometer_data = self.client.getBarometerData()
        s = pprint.pformat(barometer_data)
        print("barometer_data: %s" % s)

    def getMagnetometerData(self):
        magnetometer_data = self.client.getMagnetometerData()
        s = pprint.pformat(magnetometer_data)
        print("magnetometer_data: %s" % s)

    def getGPSData(self):
        gps_data = self.client.getGpsData()
        s = pprint.pformat(gps_data)
        print("gps_data: %s" % s)

    # getCoordinates() returns the location of the drone as a tuple
    def getCoordinates(self):
        state = self.client.getMultirotorState()
        position = state.kinematics_estimated.position
        x = position.x_val
        y = position.y_val
        z = position.z_val
        return (x, y, z)

    # takeoff() will wait for the user to press a key before arming the drone and asynchronously taking off

    async def takeoff(self):
        airsim.wait_key("Press any key to takeoff")
        print("Taking off...")
        self.client.armDisarm(True)
        await self.client.takeoffAsync().join_async()

    # moveTo() will move the drone to the given x, y, z coordinate at given speed (s) meters/second

    async def moveTo(self, x, y, z, s):
        print(f"Moving vehicle to ({x}, {y}, {z}) at {s} m/s")
        await self.client.moveToPositionAsync(x, y, z, s).join_async()
        await self.client.hoverAsync().join_async()
        await asyncio.sleep(2)

    # land() will land the drone, disarm it, and disable api control

    async def land(self):
        airsim.wait_key("Press any key to land vehicle")
        await self.client.landAsync().join_async()
        self.client.armDisarm(False)

        self.client.enableApiControl(False)

    def isLanded(self):
        return (
            self.client.getMultirotorState().landed_state == airsim.LandedState.Landed
        )

    # reset() will reset the client to where it started and disable api control

    def reset(self):
        airsim.wait_key("Press any key to reset to original state")

        self.client.reset()
        self.client.landAsync().join()
        # disarm the drone
        self.client.armDisarm(False)
        # Disables Api control
        self.client.enableApiControl(False)

    # captureImage() will capture an image from the drone and save it to a specified directory.

    def captureImage(
        self,
        image_type=airsim.ImageType.Scene,
        camera_name="0",
        vehicle_name="",
        save_dir="images",
        image_name=None,
    ):
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

        # save_dir = "\Users\renta\OneDrive\Documents\Images"
        # Create the directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)

        # Capture image
        with lock:
            response = self.client.simGetImage(
                camera_name, image_type, vehicle_name=vehicle_name
            )

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

    # WASD Directional Controls - Moves drone in the 2D directional plane at 5 meters/second

    def moveForward(self):
        x, y, z = self.getCoordinates()
        self.client.moveToPositionAsync(x + 5, y, z, 5).join()

    def moveBackward(self):
        x, y, z = self.getCoordinates()
        self.client.moveToPositionAsync(x - 5, y, z, 5).join()

    def moveRight(self):
        x, y, z = self.getCoordinates()
        self.client.moveToPositionAsync(x, y + 5, z, 5).join()

    def moveLeft(self):
        x, y, z = self.getCoordinates()
        self.client.moveToPositionAsync(x, y - 5, z, 5).join()

    # Recording functions

    def startRecording(self):
        self.client.startRecording()

    def stopRecording(self):
        self.client.stopRecording()

    # Weather functions

    def setFog(self, p):
        self.client.simEnableWeather(True)
        self.client.simSetWeatherParameter(airsim.WeatherParameter.Fog, p)
