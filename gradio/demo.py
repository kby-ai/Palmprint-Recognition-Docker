import gradio as gr
import requests
from PIL import Image
import io
import cv2
import numpy as np

palmprint_count = 0

def compare_palmprint(frame1, frame2):
    global palmprint_count
    
    palmprint_count = palmprint_count + 1

    url = "http://127.0.0.1:8080/compare_palmprint"
    files = {'file1': open(frame1, 'rb'), 'file2': open(frame2, 'rb')}

    r = requests.post(url=url, files=files)

    html = None

    compare_result = r.json().get('compare_result')
    compare_similarity = r.json().get('compare_similarity')

    html = ("<table>"
                "<tr>"
                    "<th>Compare Result</th>"
                    "<th>Value</th>"
                "</tr>"
                "<tr>"
                    "<td>Result</td>"
                    "<td>{compare_result}</td>"
                "</tr>"
                "<tr>"
                    "<td>Similarity</td>"
                    "<td>{compare_similarity}</td>"
                "</tr>"
                "</table>".format(compare_result=compare_result, compare_similarity=compare_similarity))

    return [html]

with gr.Blocks() as demo:
    gr.Markdown(
        """
    # KBY-AI Palm-Print Recognition 
    We offer SDKs for face recognition, liveness detection(anti-spoofing), ID card recognition and ID document liveness detection. 
    We also specialize in providing outsourcing services with a variety of technical stacks like AI(Computer Vision/Machine Learning), Mobile apps, and web apps.
    
    ##### KYC Verification Demo - https://github.com/kby-ai/KYC-Verification-Demo-Android
    ##### ID Capture Web Demo - https://id-document-recognition-react-alpha.vercel.app
    """
    )

    with gr.TabItem("Palmprint Recognition"):
        gr.Markdown(
            """
        ##### Docker Hub - https://hub.docker.com/r/kbyai/palmprint-recognition
        ```bash
        sudo docker pull kbyai/palmprint-recognition:latest
        sudo docker run -v ./license.txt:/root/kby-ai-palmprint/license.txt -p 8081:8080 -p 9001:9000 kbyai/palmprint-recognition:latest
        ```
        """
        )
        with gr.Row():
            with gr.Column():
                compare_palmprint_input1 = gr.Image(type='filepath')
                gr.Examples(['palmprint_examples/1.jpg', 'palmprint_examples/3.jpg', 'palmprint_examples/5.jpg', 'palmprint_examples/7.jpg'], 
                            inputs=compare_palmprint_input1)
                compare_palmprint_button = gr.Button("Compare Hand")
            with gr.Column():
                compare_palmprint_input2 = gr.Image(type='filepath')
                gr.Examples(['palmprint_examples/2.jpg', 'palmprint_examples/4.jpg', 'palmprint_examples/6.jpg', 'palmprint_examples/8.jpg'], 
                            inputs=compare_palmprint_input2)
            with gr.Column():
                compare_result_output = gr.HTML(label='Result')

        compare_palmprint_button.click(compare_palmprint, inputs=[compare_palmprint_input1, compare_palmprint_input2], outputs=[compare_result_output])
    gr.HTML('<a href="https://visitorbadge.io/status?path=https%3A%2F%2Fweb.kby-ai.com%2F"><img src="https://api.visitorbadge.io/api/combined?path=https%3A%2F%2Fweb.kby-ai.com%2F&label=VISITORS&countColor=%23263759" /></a>')

demo.launch(server_name="0.0.0.0", server_port=7860)