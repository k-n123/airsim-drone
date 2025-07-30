from hailo_platform import VDevice
from hailo_platform import HEF
from hailo_platform import InferVStreams
import cv2
import numpy as np

# 1. Load your model HEF
hef_path = "yolov6n.hef"
hef = HEF(hef_path)
