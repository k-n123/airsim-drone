from pathlib import Path

import os
import numpy as np
import cv2
import hailo

from hailo_apps.hailo_app_python.core.common.buffer_utils import (
    get_caps_from_pad,
    get_numpy_from_buffer,
    numpy_to_buffer,
)
from hailo_apps.hailo_app_python.core.gstreamer.gstreamer_app import app_callback_class
from hailo_apps.hailo_app_python.apps.detection.detection_pipeline import (
    DetectionPipeline,
)

# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class

IMAGES_FOLDER = os.path.expanduser("~/Desktop/AirSimImages/")
OUTPUT_FILE = os.path.join(IMAGES_FOLDER, "output.txt")


pipeline = DetectionPipeline()
pipeline.activate()


with open(OUTPUT_FILE, "w") as f_out:
    for img_path in sorted(Path(IMAGES_FOLDER).glob("*.png")):
        image = cv2.imread(str(img_path))
        if image is None:
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        buffer = numpy_to_buffer(image_rgb)

        roi = pipeline.run_on_buffer(buffer)
        detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

        f_out.write(f"{img_path.name}:\n")
        for det in detections:
            label = det.get_label()
            bbox = det.get_bbox()
            confidence = det.get_confidence()
            f_out.write(f"{label}, {confidence:.2f}\n")
        f_out.write("\n")

pipeline.deactivate()
print(f"detections saved to {OUTPUT_FILE}")
