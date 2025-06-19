import keyboard
from drone_commands import Drone

drone = Drone()

keyboard.add_hotkey('t', drone.takeoff())

# WASD Directional Controls
keyboard.add_hotkey('w', drone.moveForward())
keyboard.add_hotkey('s', drone.moveBackward())
keyboard.add_hotkey('a', drone.moveLeft())
keyboard.add_hotkey('d', drone.moveRight())


keyboard.wait('esc')