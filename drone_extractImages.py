import time
import os
import threading
import datetime
from drone_commands import Drone, lock
import asyncio

drone = Drone("192.168.86.48")
stop_event = asyncio.Event()


async def capture_images():
    image_dir = os.path.expanduser("~/Desktop/AirsimImages/")
    image_dir += datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "/"
    os.makedirs(image_dir, exist_ok=True)
    print("Saving images to:", image_dir)

    count = 0
    print(stop_event.is_set())

    while not stop_event.is_set():
        print("loop")
        with lock:
            result = await drone.captureImage(
                save_dir=image_dir, image_name=f"{count}.png"
            )
        print(f"Captured image {count}.png")
        count += 1
        await asyncio.sleep(1)

    print(f"{count} Images captured.")


async def main():
    # Take off first
    with lock:
        await drone.takeoff()

    # Start image capture thread
    image_task = asyncio.create_task(capture_images())

    try:
        with lock:
            print("moving")
            await drone.moveTo(0, 5, -10, 2)

        await asyncio.sleep(2)
        input("Press Enter to stop image capture and land...")
    finally:
        print("finally")
        stop_event.set()
        await image_task

        with lock:
            await drone.land()
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
