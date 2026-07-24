from flask import Flask, request, jsonify
from pipeline import run_pipeline
import requests
import threading
import time
import os

app = Flask(__name__)

NODE_URL = "http://localhost:5000/api/ocr"

FRAME_FOLDER = "frames"
BED_ID = "1"


@app.post("/detect")
def detect():

    data = request.get_json()

    image = data["image"]
    bedId = data["bedId"]

    patient = run_pipeline(image)

    if patient is None:
        return jsonify({
            "error": "Monitor not detected"
        }), 404

    payload = {
        "bedId": bedId,
        "ocr": patient
    }

    try:
        requests.post(NODE_URL, json=payload)
    except Exception as e:
        print("Cannot connect to Node:", e)

    return jsonify(patient)


def auto_process_frames():

    while True:

        try:

            images = sorted([
                f for f in os.listdir(FRAME_FOLDER)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ])

            for image in images:

                image_path = os.path.join(FRAME_FOLDER, image)

                print(f"\nProcessing: {image}")

                patient = run_pipeline(image_path)

                if patient:

                    payload = {
                        "bedId": BED_ID,
                        "ocr": patient
                    }

                    try:
                        requests.post(NODE_URL, json=payload)
                        print("Dashboard Updated")
                    except Exception as e:
                        print("Node connection failed:", e)

                else:
                    print("Monitor not detected")

                time.sleep(1)

        except Exception as e:
            print("Auto Runner Error:", e)
            time.sleep(2)


if __name__ == "__main__":

    threading.Thread(
        target=auto_process_frames,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )