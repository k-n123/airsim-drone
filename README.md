# airsim-drone


# airsim folder is the API
# settings.json contains settings for multirotor flight
# drone_commands.py contains commands 

Steps:

Installing software:
- git clone https://github.com/microsoft/AirSim.git
- pip install airsim (I recommend manually installing becuase the command will produce errors)
- Download airsim binaries

Running the simulation:
- Open an airsim binary (AirsimNH recommended) or an unreal engine project updated with the AirSim plugin
- **from drone_commands import drone** add to control file
- use functions from **drone** class to control drone

ROS:
- *wsl --install* on windows computer
- Open Ubuntu
- sudo apt update
- sudo apt install curl gnupg lsb-release
- sudo add ros repsoitory from packages.ros.org
- Add the ROS key
- Install ROS Noetic Desktop
