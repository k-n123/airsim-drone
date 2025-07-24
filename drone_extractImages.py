# import time
# import os
# import threading
# import datetime
# from drone_commands import Drone, lock
# import asyncio

# drone = Drone("192.168.86.48")
# stop_event = asyncio.Event()


# async def capture_images():
#     image_dir = os.path.expanduser("~/Desktop/AirsimImages/")
#     image_dir += datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "/"
#     os.makedirs(image_dir, exist_ok=True)
#     print("Saving images to:", image_dir)

#     count = 0
#     print(stop_event.is_set())

#     while not stop_event.is_set():
#         print("loop")
#         with lock:
#             result = await drone.captureImage(
#                 save_dir=image_dir, image_name=f"{count}.png"
#             )
#         print(f"Captured image {count}.png")
#         count += 1
#         await asyncio.sleep(1)

#     print(f"{count} Images captured.")


# async def main():
#     # Take off first
#     with lock:
#         await drone.takeoff()

#     # Start image capture thread
#     image_task = asyncio.create_task(capture_images())

#     try:
#         with lock:
#             print("moving")
#             await drone.moveTo(0, 5, -10, 2)

#         await asyncio.sleep(2)
#         input("Press Enter to stop image capture and land...")
#     finally:
#         print("finally")
#         stop_event.set()
#         await image_task

#         with lock:
#             await drone.land()
#         print("Done.")


# if __name__ == "__main__":
#     asyncio.run(main())

import airsim
import os
import asyncio
import datetime


class Drone:
    def __init__(self, ip="192.168.86.48"):
        self.client = airsim.MultirotorClient(ip=ip)
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

    async def takeoff(self):
        print("Taking off...")
        await asyncio.to_thread(self.client.takeoffAsync().join)
        await asyncio.to_thread(self.client.hoverAsync().join)

    async def land(self):
        print("Landing...")
        await asyncio.to_thread(self.client.landAsync().join)
        self.client.armDisarm(False)
        self.client.enableApiControl(False)

    async def move_to(self, x, y, z, speed):
        print(f"Moving to ({x}, {y}, {z}) at {speed} m/s")
        await asyncio.to_thread(self.client.moveToPositionAsync(x, y, z, speed).join)

    async def capture_image_loop(self, stop_event: asyncio.Event, save_dir: str):
        count = 0
        print(f"Saving images to: {save_dir}")
        os.makedirs(save_dir, exist_ok=True)

        while not stop_event.is_set():
            responses = self.client.simGetImages(
                [airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)]
            )
            if responses:
                image_data = responses[0].image_data_uint8
                if image_data:
                    file_path = os.path.join(save_dir, f"image_{count:04d}.png")
                    with open(file_path, "wb") as f:
                        f.write(image_data)
                    print(f"Captured {file_path}")
                    count += 1
            await asyncio.sleep(1)

        print(f"Stopped capturing after {count} images.")


async def main():
    drone = Drone()
    stop_event = asyncio.Event()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_dir = os.path.expanduser(f"~/Desktop/AirSimImages/{timestamp}")

    await drone.takeoff()

    # Start image capture loop in the background
    image_task = asyncio.create_task(drone.capture_image_loop(stop_event, image_dir))

    try:
        # Example movement path
        await drone.move_to(0, 10, -5, 2)
        await asyncio.sleep(1)
        await drone.move_to(10, 10, -5, 2)
        await asyncio.sleep(1)
        await drone.move_to(10, 0, -5, 2)
        await asyncio.sleep(1)
        await drone.move_to(0, 0, -5, 2)

    finally:
        stop_event.set()
        await image_task
        await drone.land()


if __name__ == "__main__":
    asyncio.run(main())
