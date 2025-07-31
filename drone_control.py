from drone_commands import Drone
from drone_multipleDrones import MultipleDroneController

controller = MultipleDroneController("192.168.86.29", ["Drone1", "Drone2"])

controller.takeoffAll()

controller.up(20, "Drone1")
controller.up(20, "Drone2")

controller.moveAll(10, controller.forward)

controller.landAll()
controller.resetAll()
