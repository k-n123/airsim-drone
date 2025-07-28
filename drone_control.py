from drone_commands import Drone

drone = Drone("192.168.86.35")

drone.takeoff()

drone.forward(10)
drone.right(5)

drone.land()
