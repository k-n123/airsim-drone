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

On Raspberry Pi 5:
- Flash 64-bit OS
- Install Python3, pip, venv
- Create venv with python3 -m venv airsim-env
- Activate venv with source airsim-env/bin/activate
- pip install msgpack-rpc-python numpy opencv-python
- pip install airsim > Install after others
- ```client = airsim.MultirotorClient(ip="192.168.1.100", port=41451)``` will allow for the Raspberry Pi to connect the simulation. Make sure to use proper IP address of simulation
