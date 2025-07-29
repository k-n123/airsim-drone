import setup_path
import airsim

import os
import time
import cv2
import numpy as np


class MultipleDroneController:
    def __init__(self, ip_add, names):
        self.client = airsim.MultirotorClient(ip=ip_add, port=41451)
        self.client.confirmConnection()
        self.droneNames = names

        for name in names:
            self.client.enableApiControl(True, name)

    def waitOnAllTasks(self, futures):
        """
        Waits for all tasks to complete.
        """
        for future in futures:
            future.join()

    def takeoffAll(self):
        futures = []
        for name in self.droneNames:
            self.client.enableApiControl(True, name)
            self.client.armDisarm(True, name)
            futures.append(self.client.takeoffAsync(vehicle_name=name))
        self.waitOnAllTasks(futures)

    def takeoff(self, name):
        print("Taking off...")
        self.client.enableApiControl(True, name)
        self.client.armDisarm(True, name)
        self.client.takeoffAsync(vehicle_name=name).join()

    def landAll(self):
        futures = []
        for name in self.droneNames:
            futures.append(self.client.landAsync(vehicle_name=name))
            self.client.armDisarm(False, name)
            self.client.enableApiControl(False, name)
        self.waitOnAllTasks(futures)

    def land(self, name):
        print("Landing...")
        self.client.landAsync(vehicle_name=name).join()
        self.client.armDisarm(False, name)
        self.client.enableApiControl(False, name)

    def resetAll(self):
        futures = []
        for name in self.droneNames:
            futures.append(self.client.reset(vehicle_name=name))
            self.client.enableApiControl(False, name)
        self.waitOnAllTasks(futures)

    def reset(self, name):
        print("Resetting drone...")
        self.client.reset(vehicle_name=name)
        self.client.enableApiControl(False, name)

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

    def captureImageAll(self, image_type=airsim.ImageType.Scene, camera_name="0"):
        path = os.path.expanduser("~/Desktop/AirSimImages/")
        for name in self.droneNames:
            self.captureImage(
                image_type=image_type,
                camera_name=camera_name,
                vehicle_name=name,
                save_dir=path,
                image_name=f"{name}_image.png",
            )

    def getCoordinates(self, name):
        state = self.client.getMultirotorState(vehicle_name=name)
        position = state.kinematics_estimated.position
        x = position.x_val
        y = position.y_val
        z = position.z_val
        return (x, y, z)

    def forward(self, distance, name):
        x, y, z = self.getCoordinates(name)
        path = os.path.expanduser("~/Desktop/AirSimImages/")
        for i in range(distance):
            self.client.moveToPositionAsync(x + i, y, z, 2).join()
            self.captureImage(
                camera_name="BottomCamera",
                save_dir=path,
                image_name=f"{name} forward_{i}.png",
            )

    def backward(self, distance, name):
        x, y, z = self.getCoordinates(name)
        path = os.path.expanduser("~/Desktop/AirSimImages/")
        for i in range(distance):
            self.client.moveToPositionAsync(x - i, y, z, 2).join()
            self.captureImage(save_dir=path, image_name=f"{name} backward_{i}.png")

    def left(self, distance, name):
        x, y, z = self.getCoordinates(name)
        path = os.path.expanduser("~/Desktop/AirSimImages/")
        for i in range(distance):
            self.client.moveToPositionAsync(x, y - i, z, 2).join()
            self.captureImage(save_dir=path, image_name=f"{name} left_{i}.png")

    def right(self, distance, name):
        x, y, z = self.getCoordinates(name)
        path = os.path.expanduser("~/Desktop/AirSimImages/")
        for i in range(distance):
            self.client.moveToPositionAsync(x, y + i, z, 2).join()
            self.captureImage(save_dir=path, image_name=f"{name} right_{i}.png")

    def moveAll(self, distance, func):
        # Execute a movement function for ALL drones
        for name in self.droneNames:
            func(distance, name)
