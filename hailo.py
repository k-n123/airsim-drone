from hailo_platform import VDevice
from hailo_platform import HEF
from hailo_platform import InferVStreams
import cv2
import numpy as np
import os

# 1. Load your model HEF
hef_path = "yolov6n.hef"
hef = HEF(hef_path)


# 2. Create virtual device
with VDevice() as device:
    # 3. Configure network group
    network_groups = device.configure(hef)
    network_group = network_groups[0]

    # 4. Create input/output streams
    input_vstream_info = hef.get_input_vstream_infos()
    output_vstream_info = hef.get_output_vstream_infos()
    with InferVStreams(
        network_group, input_vstream_info, output_vstream_info
    ) as infer_vstreams:

        # 5. Load an image
        path = os.expanduser("~/Desktop/AirSimImages/")
        image_path = os.path.join(path, "Drone1 forward_0.png")
        img = cv2.imread(image_path)
        img_resized = cv2.resize(img, (640, 640))  # depends on model
        img_resized = img_resized.astype(np.float32)

        # 6. Run inference
        infer_results = infer_vstreams.infer([img_resized])

        # 7. Process results
        print("Inference output:", infer_results)
