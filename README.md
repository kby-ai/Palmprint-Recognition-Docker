<p align="center">
  <a href="https://play.google.com/store/apps/dev?id=7086930298279250852" target="_blank">
    <img alt="" src="https://github-production-user-asset-6210df.s3.amazonaws.com/125717930/246971879-8ce757c3-90dc-438d-807f-3f3d29ddc064.png" width=500/>
  </a>  
</p>

#### 🤗 Hugging Face - [Here](https://huggingface.co/kby-ai) <span> <img src="https://github.com/kby-ai/.github/assets/125717930/bcf351c5-8b7a-496e-a8f9-c236eb8ad59e" style="margin: 4px; width: 36px; height: 20px"> <span/>
#### 📚 Product & Resources - [Here](https://github.com/kby-ai/Product)
#### 🛟 Help Center - [Here](https://docs.kby-ai.com)
#### 💼 KYC Verification Demo - [Here](https://github.com/kby-ai/KYC-Verification-Demo-Android)
#### 🙋‍♀️ Docker Hub - [Here](https://hub.docker.com/r/kbyai/palmprint-recognition)
```bash
sudo docker pull kbyai/palmprint-recognition:latest
sudo docker run -v ./license.txt:/root/kby-ai-palmprint/license.txt -p 8081:8080 -p 9001:9000 kbyai/palmprint-recognition:latest
```

# Palmprint Recognition-Docker
## Overview
This repository demonstrates an efficient and accurate palmprint recognition technology by implementing palm-print comparison based on palmprint feature extraction and face matching algorithm, which was implemented via a `Dockerized Flask API`.<br/>
It includes features that allow for testing plamprint recognition between two images using both image files and `base64-encoded` images.

> In this repo, we integrated `KBY-AI`'s palmprint recognition solution into `Linux Server SDK` by wrapping with docker image.<br/>
> We can customize the SDK to align with customer's specific requirements.

### ◾PalmRecognitionSDK Product List
  | No.      | Repository | SDK Details | Status |
  |------------------|------------------|------------------|------------------|
  | ➡️        | <b>[Palmprint Recognition - Linux](https://github.com/kby-ai/Palmprint-Recognition-Linux)</b>    | <b>Palmprint Comparison Linux SDK</b> | <b>Available</b> |
  | 2        | [Palmprint Recognition - Docker](https://hub.docker.com/r/kbyai/palmprint-recognition)    | Palmprint Comparison Docker Image | Available |
  | 3        | Palmvein Recognition - Linux    | Palmvein Comparison Linux SDK | Developing |
  | 4        | [Palmprint Recognition - Android](https://github.com/kby-ai/Palmprint-Recognition-Android)    | Palmprint Comparison Android SDK | Available |
  | 5        | Palmprint Recognition - iOS    | Palmprint Comparison iOS SDK | Developing |

> To get more products, please visit products [here](https://github.com/kby-ai):<br/>

## Try the API
### Online Demo
  This `SDK` can be tested on online test demo page [here](https://web.kby-ai.com):
  > Please select tab 'Palmprint Recognition` for this SDK
  
  ![image](https://github.com/user-attachments/assets/4e660694-f5bf-4f00-be2b-822c093e2d94)
  
### Postman
  The `API` can be evaluated through `Postman` tool. Here are the endpoints for testing:
  - Test with an image file: Send a `POST` request to `http://89.116.159.229:8084/compare_palmprint`.
  - Test with a `base64-encoded` image: Send a `POST` request to `http://89.116.159.229:8084/compare_palmprint_base64`.
    
    ![image](https://github.com/user-attachments/assets/4c5a528d-572c-46fe-b2de-6f387929b181)

## SDK License

This project demonstrates `KBY-AI`'s `Palmprint Recognition Server SDK`, which requires a license per machine.

- The code below shows how to use the license: https://github.com/kby-ai/Palmprint-Recognition-Docker/blob/290f714ca49496164f0586f277b6104bfd164ad7/app.py#L21-L31

- To request the license, please provide us with the `machine code` obtained from the `getMachineCode` function.

#### Please contact us:</br>
🧙`Email:` contact@kby-ai.com</br>
🧙`Telegram:` [@kbyai](https://t.me/kbyai)</br>
🧙`WhatsApp:` [+19092802609](https://wa.me/+19092802609)</br>
🧙`Skype:` [live:.cid.66e2522354b1049b](https://join.skype.com/invite/OffY2r1NUFev)</br>
🧙`Facebook:` https://www.facebook.com/KBYAI</br>
  
## How to run

### 1. System Requirements
  - `CPU`: 2 cores or more (Recommended: 2 cores)
  - `RAM`: 4 GB or more (Recommended: 8 GB)
  - `HDD`: 4 GB or more (Recommended: 8 GB)
  - `OS`: `Ubuntu 20.04` or later
  - Dependency: `OpenVINO™ Runtime` (Version: 2022.3)

### 2. Setup and Test
  - Clone the project:
    ```bash
    git clone https://github.com/kby-ai/Palmprint-Recognition-Docker.git
    ```
    ```bash
    cd Palmprint-Recognition-Docker
    ```
  - Build the `Docker` image:
    ```bash
    sudo docker build --pull --rm -f Dockerfile -t kby-ai-palmprint:latest .
    ```
  - Run the `Docker` container:
    ```bash
    sudo docker run -v ./license.txt:/root/kby-ai-palmprint/license.txt -p 8081:8080 -p 9001:9000 kby-ai-palmprint
    ```
  - Send us the `machine code` and then we will give you a license key to make the `SDK` activate.
  
    After that, update the `license.txt` file by overwriting the `license key` that you received. Then, run the `Docker` container again.

    ![image](https://github.com/user-attachments/assets/08865793-ee4e-4ede-aaf1-8fa70a8d8faa)
    
    ![image](https://github.com/user-attachments/assets/194b8666-8638-4ffc-8ee3-63f2ba491763)

  - Here are the endpoints to test the `API` through `Postman`:

    Test with an image file: Send a `POST` request to `http://{xx.xx.xx.xx}:8081/compare_palmprint`.
    
    Test with a `base64-encoded` image: Send a `POST` request to `http://{xx.xx.xx.xx}:8081/compare_palmprint_base64`.

### 3. Execute the Gradio demo
  - Setup `Gradio`
    Ensure that the necessary dependencies are installed. </br>
    `Gradio` requires `Python 3.6` or above. </br>
    Install `Gradio` using `pip` by running the following command:
    ```bash
    pip install gradio
    ```
  - Run the demo with the following command:
    ```bash
    cd gradio
    python demo.py
    ```
  - `SDK` can be tested on the following URL: `http://127.0.0.1:9000`

## About SDK

### 1. Initializing the SDK

- Import SDK python package
  ```python
  import handtool
  ```
- Create new object for using `SDK` 
  ```python
  config = handtool.EncoderConfig()
  encoder = handtool.create_encoder(config)  
  ```
- Obtain the `machine code` to activate and request a license
  ```python
  machineCode = encoder.getMachineCode()
  print("\nmachineCode: ", machineCode.decode('utf-8'))
  ```
- Activate the `SDK` using the license key
  ```python
  ret = encoder.setActivation(license.encode('utf-8'))
  print("\nactivation: ", ret)
  ```  
  Once `ret` value is zero, SDK can get work started

### 2. APIs
  - Hand Detection
  
    The `SDK` provides a single API for detecting hands, determining `hand landmark`.</br>
    The function can be used as follows:
    ```python
    hand_type, x1, y1, x2, y2, detect_state = encoder.detect_using_bytes(img)
    roi = mat_to_bytes(get_roi(img, hand_type, x1, y1, x2, y2))
    ```
    * `hand_type`: it indicates hand type value, `0` value: `left hand`, `1` value: `right hand`.
    * `x1`, `y1`, `x2`, `y2`: hand landmark points to get `ROI` image.
    * `roi`: hand `ROI(Region Of Interest)` image to get palm feature.
  - Create Feature
    `encode_using_bytes` function returns palmprint feature against `ROI` data.</br.
    ```python    
    palmprint = encoder.encode_using_bytes(roi)
    ```
    * `roi`: hand `ROI(Region Of Interest)` image to get palm feature.
    * `palmprint`: palmprint feature calculated from hand `ROI` data.    
  - Similiarity
    The `compare_to` function takes two palmprint `feature`s as a parameter and returns `score` value to determine whether 2 input hands are from the same or different.
    ```python
    one_palmprint_code = encoder.encode_using_bytes(roi1)
    another_palmprint_code = encoder.encode_using_bytes(roi2)
    score = one_palmprint_code.compare_to(another_palmprint_code)
    ```

### 3. Threshold
  The threshold is `0.15` as a default.
  https://github.com/kby-ai/Palmprint-Recognition-Docker/blob/ddf1f039c55534d7189fda162b5c4df844131b72/app.py#L12-L13

