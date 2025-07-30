from hailo_platform import VDevice, HEF, InferVStreams
import cv2
import numpy as np
import os


# Path to YOLOv6n HEF
hef_path = "yolov6n.hef"

# Path to input image
path = os.expanduser("~/Desktop/AirSimImages/")
image_path = os.path.join(path, "Drone1 forward_0.png")

# Preprocessing parameters (adjust to model input)
MODEL_INPUT_SIZE = (640, 640)  # YOLOv6n


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, MODEL_INPUT_SIZE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # YOLO expects RGB
    img = img.astype(np.float32) / 255.0  # normalize
    img = np.transpose(img, (2, 0, 1))  # CHW format
    return img


# Preprocess image
input_image = preprocess_image(image_path)

# Hailo expects a list of numpy arrays as batch
input_batch = [input_image]

hef = HEF(hef_path)

with VDevice() as device:
    # 1. Configure network
    network_group = device.configure(hef)[0]

    # 2. Get stream infos
    input_infos = hef.get_input_vstream_infos()
    output_infos = hef.get_output_vstream_infos()

    # 3. Convert to params
    input_params = {
        info.name: InferVStreams.create_input_params(info) for info in input_infos
    }
    output_params = {
        info.name: InferVStreams.create_output_params(info) for info in output_infos
    }

    # 4. Run inference
    with InferVStreams(network_group, input_params, output_params) as infer_vstreams:
        results = infer_vstreams.infer(input_batch)

# results is a dictionary of {output_name: np.array}
print("Raw YOLOv6 outputs:")
for name, tensor in results.items():
    print(name, tensor.shape)
