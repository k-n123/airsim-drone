import asyncio
from drone_commands import Drone, lock
import os
import datetime

drone = Drone("192.168.86.48")


async def capture_images_async(stop_event):
    savedir = os.path.expanduser("~/Desktop/AirsimImages/")
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    savedir = os.path.join(savedir, date)
    print(f"Started async image capture loop. Saving to: {savedir}")
    loop = asyncio.get_running_loop()
    while not stop_event.is_set():

        def capture():
            with lock:
                return drone.captureImage(save_dir=savedir)

        result = await loop.run_in_executor(None, capture)
        if result is None:
            print("Image capture failed.")
        else:
            print(f"Image captured and saved to: {result}")
        await asyncio.sleep(0.5)
    print("Stopped async image capture loop.")


async def main():
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    def takeoff():
        with lock:
            drone.takeoff()

    await loop.run_in_executor(None, takeoff)

    # Start image capture task
    capture_task = asyncio.create_task(capture_images_async(stop_event))

    def move_commands():
        with lock:
            drone.moveTo(20, 20, -20, 3)
            drone.moveTo(-5, -5, -10, 3)

    await loop.run_in_executor(None, move_commands)

    input("Press Enter to stop capturing images and land the drone...")
    stop_event.set()
    await capture_task

    def land():
        with lock:
            drone.land()

    await loop.run_in_executor(None, land)
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
