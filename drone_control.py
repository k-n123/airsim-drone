from drone_commands import Drone # Importing the drone class

drone = Drone() # Initialize drone

drone.takeoff()

# Further actions here

drone.moveForward()
drone.moveRight()
drone.moveBackward()
drone.moveLeft()

drone.reset()