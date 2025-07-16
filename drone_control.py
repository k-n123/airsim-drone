from drone_commands import Drone # Importing the drone class

drone = Drone() # Initialize drone

drone.takeoff()

# Further actions here
drone.moveTo(10, 10, -10, 2)


drone.reset()