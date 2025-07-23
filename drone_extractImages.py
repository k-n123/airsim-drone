import time
import os
import threading
import datetime
from drone_commands import Drone, lock

drone = Drone("192.168.86.48")
stop_event = threading.Event()


def capture_images():
    image_dir = os.path.expanduser("~/Desktop/AirsimImages/")
    image_dir += datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "/"
    os.makedirs(image_dir, exist_ok=True)
    print("Saving images to:", image_dir)

    count = 0
    while not stop_event.is_set():
        with lock:
            result = drone.captureImage(save_dir=image_dir, image_name=f"{count}.png")
        print(f"Captured image {count}.png")
        count += 1
        time.sleep(1)

    print(f"{count} Images captured.")


def main():
    # Take off first
    with lock:
        drone.takeoff()

    # Start image capture thread
    image_thread = threading.Thread(target=capture_images, daemon=True)
    image_thread.start()

    try:
        with lock:
            drone.moveTo(0, 5, -10, 2)
        time.sleep(2)
        with lock:
            drone.moveForward()
        time.sleep(2)
        input("Press Enter to stop image capture and land...")
    finally:
        stop_event.set()
        image_thread.join()
        with lock:
            drone.land()
        print("Done.")

    drone.reset()


if __name__ == "__main__":
    main()
