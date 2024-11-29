# palm-print recognition demo inference against 2 hand images. 
import os
import handtool
import cv2
from roi import get_roi

threshold = 0.15

def mat_to_bytes(mat):
    """
    Convert cv::Mat image data (NumPy array in Python) to raw bytes.
    """
    # Encode cv::Mat as PNG bytes
    is_success, buffer = cv2.imencode(".png", mat)
    if not is_success:
        raise ValueError("Failed to encode cv::Mat image")
    return buffer.tobytes()

def infer(path_1, path_2):
    config = handtool.EncoderConfig(29, 5, 5, 10)
    encoder = handtool.create_encoder(config)

    licensePath = "license.txt"
    license = ""

    machineCode = encoder.getMachineCode()
    print("\nmachineCode: ", machineCode.decode('utf-8'))

    try:
        with open(licensePath, 'r') as file:
            license = file.read()
    except IOError as exc:
        print("failed to open license.txt: ", exc.errno)
    print("\nlicense: ", license)

    ret = encoder.setActivation(license.encode('utf-8'))
    print("\nactivation: ", ret)

    _ = encoder.init()

    hand_type_1, x11, y11, x12, y12, detect_state_1 = encoder.detect_using_file(path_1)
    hand_type_2, x21, y21, x22, y22, detect_state_2 = encoder.detect_using_file(path_2)

    if hand_type_1 != hand_type_2:
        print("*" * 100)
        print(f"\n 2 images are from the different hand\n similarity: 0.0")
        return
    if detect_state_1 == 0 or detect_state_2 == 0:
        if ret != 0:
            return
        print("*" * 100)
        print(f"\n hand detection failed !\n plesae make sure that input hand image is valid or not.")
        return
    if detect_state_1 >= 2 or detect_state_2 >= 2:
        print(f"\n multi-hand detected !\n plesae put one hand image, not multiple hand.")
        return
    roi_1 = get_roi(path_1, hand_type_1, x11, y11, x12, y12)
    roi_2 = get_roi(path_2, hand_type_2, x21, y21, x22, y22)
    # cv2.imwrite("1.jpg", roi_1)
    
    roi_1 = mat_to_bytes(roi_1)
    roi_2 = mat_to_bytes(roi_2)
    one_palmprint_code = encoder.encode_using_bytes(roi_1)
    another_palmprint_code = encoder.encode_using_bytes(roi_2)
    score = one_palmprint_code.compare_to(another_palmprint_code)

    print("*" * 100)
    if score >= threshold:
        print(f"\n 2 images are from the same hand\n similarity: {score}")
    else:
        print(f"\n 2 images are from the different hand\n similarity: {score}")

if __name__ == "__main__":

    path_1 = "img/person2/00071.tiff"
    path_2 = "img/person5/3.jpg"

    infer(path_1, path_2)    
