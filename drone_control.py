from drone_commands import Drone
from drone_multipleDrones import MultipleDroneController

controller = MultipleDroneController("10.74.226.210", ["Drone1", "Drone2"])

controller.takeoffAll()


controller.moveAll(10, controller.forward)

controller.landAll()
