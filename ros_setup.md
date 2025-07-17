# ROS Setup Instructions

After downloading Ubuntu 20.04 from the web

## 1. Ensure you're on Ubuntu 20.04
lsb_release -a

## 2. Install necessary tools
sudo apt update
sudo apt install curl gnupg2 lsb-release ca-certificates -y

## 3. Add the ROS 1 GPG key and sources securely
sudo mkdir -p /etc/apt/keyrings
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    | sudo tee /etc/apt/keyrings/ros-archive-keyring.gpg > /dev/null

echo "deb [signed-by=/etc/apt/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" \
| sudo tee /etc/apt/sources.list.d/ros-latest.list > /dev/null

## 4. Update apt and install ROS Noetic
sudo apt update
sudo apt install ros-noetic-desktop-full -y

## 5. Add to your shell environment
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

## 6. Initialize rosdep
sudo apt install python3-rosdep -y
sudo rosdep init
rosdep update

## 7. Initialize catkin
sudo apt install catkin
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make

## 8. Build Airsim ROS bridge inside Catkin
cd ~/catkin_ws/src
git clone https://github.com/microsoft/AirSim.git
cd ~/catkin_ws
catkin_make

