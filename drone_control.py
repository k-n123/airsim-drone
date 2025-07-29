from drone_commands import Drone

drone = Drone("10.74.226.210")

drone.takeoff()

drone.forward(10)
drone.right(5)

drone.land()
