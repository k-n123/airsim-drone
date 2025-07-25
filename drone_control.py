from drone_commands import Drone  # Importing the drone class
import keyboard

drone = Drone("192.168.86.48")  # Initialize drone

drone.takeoff()

currentKey = "w"

while not drone.isLanded():
    if currentKey == "w":
        drone.moveForward()
    elif currentKey == "s":
        drone.moveBackward()
    elif currentKey == "a":
        drone.moveLeft()
    elif currentKey == "d":
        drone.moveRight()
    elif currentKey == "q":
        drone.moveUp()
    elif currentKey == "e":
        drone.moveDown()
    elif currentKey == "backspace":
        drone.reset()
        break
    else:
        drone.land()
        break

    drone.captureImage(save_dir="~/Desktop/AirSimImages/", image_name="image.png")

    if keyboard.is_pressed("w"):
        currentKey = "w"
    elif keyboard.is_pressed("s"):
        currentKey = "s"
    elif keyboard.is_pressed("a"):
        currentKey = "a"
    elif keyboard.is_pressed("d"):
        currentKey = "d"
    elif keyboard.is_pressed("q"):
        currentKey = "q"
    elif keyboard.is_pressed("e"):
        currentKey = "e"
    elif keyboard.is_pressed("backspace"):
        drone.reset()
        break
    elif keyboard.is_pressed("esc"):
        drone.land()
        break
