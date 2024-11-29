import sys
sys.path.append('.')

import os
import base64
import json
import handtool
import cv2
import numpy as np
from roi import get_roi, mat_to_bytes
from flask import Flask, request, jsonify

threshold = 0.15

licensePath = "license.txt"
license = ""

config = handtool.EncoderConfig(29, 5, 5, 10)
encoder = handtool.create_encoder(config)

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
print("\ninit: ", ret)

app = Flask(__name__) 

@app.route('/compare_palmprint', methods=['POST'])
def compare_palmprint():
    result = "None"
    similarity = -1
    
    file1 = request.files['file1']
    file2 = request.files['file2']

    try:
        image1 = cv2.imdecode(np.frombuffer(file1.read(), np.uint8), cv2.IMREAD_COLOR)

    except:
        result = "Failed to open file1"
        response = jsonify({"compare_result": result, "compare_similarity": similarity})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


    try:
        image2 = cv2.imdecode(np.frombuffer(file2.read(), np.uint8), cv2.IMREAD_COLOR)
    except:
        result = "Failed to open file2"
        response = jsonify({"compare_result": result, "compare_similarity": similarity})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    
    img1 = mat_to_bytes(image1)
    img2 = mat_to_bytes(image2)
    hand_type_1, x11, y11, x12, y12, detect_state_1 = encoder.detect_using_bytes(img1)
    hand_type_2, x21, y21, x22, y22, detect_state_2 = encoder.detect_using_bytes(img2)

    if hand_type_1 != hand_type_2:
        result = "Different hand"
        # print(f"\n 2 images are from the different hand\n similarity: 0.0")
        similarity = 0.0
        response = jsonify({"compare_result": result, "compare_similarity": similarity})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
        
    if detect_state_1 == 0 or detect_state_2 == 0:
        if ret != 0:
            result = "Activation failed"
            response = jsonify({"compare_result": result, "compare_similarity": similarity})
            response.status_code = 200
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
            
        # print(f"\n hand detection failed !\n plesae make sure that input hand image is valid or not.")
        result = "hand detection failed !\nPlesae make sure that input hand image is valid or not."
        response = jsonify({"compare_result": result, "compare_similarity": similarity})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
        
    if detect_state_1 >= 2 or detect_state_2 >= 2:
        # print(f"\n multi-hand detected !\n plesae put one hand image, not multiple hand.")
        result = "multi-hand detected !\nPlesae try on image with one hand , not multiple hand."
        response = jsonify({"compare_result": result, "compare_similarity": similarity})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    roi1 = mat_to_bytes(get_roi(image1, hand_type_1, x11, y11, x12, y12))
    roi2 = mat_to_bytes(get_roi(image2, hand_type_2, x21, y21, x22, y22))
    
    one_palmprint_code = encoder.encode_using_bytes(roi1)
    another_palmprint_code = encoder.encode_using_bytes(roi2)
    score = one_palmprint_code.compare_to(another_palmprint_code)

    if score >= threshold:
        result = "Same hand"
        similarity = score
        # print(f"\n 2 images are from the same hand\n similarity: {score}")
    else:
        result = "Different hand"
        similarity = score
        # print(f"\n 2 images are from the different hand\n similarity: {score}")
    
    response = jsonify({"compare_result": result, "compare_similarity": similarity})

    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

@app.route('/compare_palmprint_base64', methods=['POST'])
def compare_palmprint_base64():
    result = "None"
    similarity = -1
    
    content = request.get_json()

    try:
        imageBase64_1 = content['base64_1']
        image_data1 = base64.b64decode(imageBase64_1) 
        np_array = np.frombuffer(image_data1, np.uint8)
        image1 = cv2.imdecode(np_array, cv2.IMREAD_COLOR)   
    except:
        result = "Failed to open file1"
        response = jsonify({"compare_result": result, "compare_similarity": similarity})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    
    try:
        imageBase64_2 = content['base64_2']
        image_data2 = base64.b64decode(imageBase64_2)
        np_array = np.frombuffer(image_data2, np.uint8)
        image2 = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    except IOError as exc:
        result = "Failed to open file2"
        response = jsonify({"compare_result": result, "compare_similarity": similarity})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    img1 = mat_to_bytes(image1)
    img2 = mat_to_bytes(image2)
    hand_type_1, x11, y11, x12, y12, detect_state_1 = encoder.detect_using_bytes(img1)
    hand_type_2, x21, y21, x22, y22, detect_state_2 = encoder.detect_using_bytes(img2)

    if hand_type_1 != hand_type_2:
        result = "Different hand"
        # print(f"\n 2 images are from the different hand\n similarity: 0.0")
        similarity = 0.0
        response = jsonify({"compare_result": result, "compare_similarity": similarity})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
        
    if detect_state_1 == 0 or detect_state_2 == 0:
        if ret != 0:
            result = "Activation failed"
            response = jsonify({"compare_result": result, "compare_similarity": similarity})
            response.status_code = 200
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
            
        # print(f"\n hand detection failed !\n plesae make sure that input hand image is valid or not.")
        result = "hand detection failed !\nPlesae make sure that input hand image is valid or not."
        response = jsonify({"compare_result": result, "compare_similarity": similarity})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
        
    if detect_state_1 >= 2 or detect_state_2 >= 2:
        # print(f"\n multi-hand detected !\n plesae put one hand image, not multiple hand.")
        result = "multi-hand detected !\nPlesae try on image with one hand , not multiple hand."
        response = jsonify({"compare_result": result, "compare_similarity": similarity})
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    roi1 = mat_to_bytes(get_roi(image1, hand_type_1, x11, y11, x12, y12))
    roi2 = mat_to_bytes(get_roi(image2, hand_type_2, x21, y21, x22, y22))
    
    one_palmprint_code = encoder.encode_using_bytes(roi1)
    another_palmprint_code = encoder.encode_using_bytes(roi2)
    score = one_palmprint_code.compare_to(another_palmprint_code)

    if score >= threshold:
        result = "Same hand"
        similarity = score
        # print(f"\n 2 images are from the same hand\n similarity: {score}")
    else:
        result = "Different hand"
        similarity = score
        # print(f"\n 2 images are from the different hand\n similarity: {score}")
    
    response = jsonify({"compare_result": result, "compare_similarity": similarity})

    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

    

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)