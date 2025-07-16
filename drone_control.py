from drone_commands import Drone # Importing the drone class

drone = Drone() # Initialize drone

drone.takeoff()

# Further actions here

drone.moveTo(20, 20, -20, 3)
drone.moveTo(-5, -5, -10, 3)

drone.reset()