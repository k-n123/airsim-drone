from drone_commands import Drone, lock

drone = Drone("192.168.86.48")

import time
import os
import threading
import datetime
import numpy as np

import asyncio


async def capture_Images():
    image_dir = os.path.expanduser("~/Desktop/AirsimImages/")
    image_dir += datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "/"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    print(image_dir)

    count = 0
    while not await drone.isLanded():
        await drone.captureImage(save_dir=image_dir, image_name=str(count) + ".png")
        count += 1
        await asyncio.sleep(1)  # capture every second

    print(str(count) + " Images captured")


async def main():
    drone.takeoff()

    asyncio.create_task(capture_Images())

    await drone.moveTo(0, 5, -10, 2)
    await asyncio.sleep(2)
    await drone.reset()


loop = asyncio.get_event_loop()
if loop.is_running():
    asyncio.create_task(main())
else:
    loop.run_until_complete(main())
