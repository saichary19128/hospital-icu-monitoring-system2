from modules.monitor_detector import detect_monitor
from modules.vital_detector import detect_vitals
from modules.ocr_reader import read_values
from modules.json_writer import save_json
from modules.utils import print_patient

import os
import time
import shutil

FRAMES_FOLDER = "frames"
PROCESSED_FOLDER = "processed"

os.makedirs(FRAMES_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def process_frame(image_path):

    print("\n====================================")
    print(f"Processing : {os.path.basename(image_path)}")
    print("====================================\n")

    total_start = time.perf_counter()

    # ----------------------------
    # Monitor Detection
    # ----------------------------
    start = time.perf_counter()

    monitor_crop = detect_monitor(image_path)

    monitor_time = time.perf_counter() - start

    if monitor_crop is None:
        print("Monitor not detected!")

        shutil.move(
            image_path,
            os.path.join(
                PROCESSED_FOLDER,
                os.path.basename(image_path)
            )
        )

        return

    # ----------------------------
    # Vital Detection
    # ----------------------------
    start = time.perf_counter()

    detections = detect_vitals(monitor_crop)

    vital_time = time.perf_counter() - start

    # ----------------------------
    # OCR
    # ----------------------------
    start = time.perf_counter()

    patient = read_values(
        detections,
        monitor_crop
    )

    ocr_time = time.perf_counter() - start

    # ----------------------------
    # Print
    # ----------------------------
    print_patient(patient)

    # ----------------------------
    # Save JSON
    # ----------------------------
    start = time.perf_counter()

    save_json(patient)

    json_time = time.perf_counter() - start

    total_time = time.perf_counter() - total_start

    print("\nPatient data saved successfully.")

    print("\n========== Performance ==========\n")

    print(f"Monitor Detection : {monitor_time:.3f} sec")
    print(f"Vital Detection   : {vital_time:.3f} sec")
    print(f"OCR               : {ocr_time:.3f} sec")
    print(f"JSON Save         : {json_time:.3f} sec")

    print("---------------------------------")
    print(f"Total Time        : {total_time:.3f} sec")

    # ----------------------------
    # Move processed frame
    # ----------------------------
    destination = os.path.join(
        PROCESSED_FOLDER,
        os.path.basename(image_path)
    )

    shutil.move(
        image_path,
        destination
    )

    print(f"\nMoved to : {destination}")


def main():

    frame_number = 1

    print("\n======================================")
    print(" ICU Monitor Stream Started")
    print("======================================\n")

    while True:

        image_path = os.path.join(
            FRAMES_FOLDER,
            f"frame{frame_number}.jpg"
        )

        if os.path.exists(image_path):

            process_frame(image_path)

            frame_number += 1

            print("\nWaiting 2 seconds for next frame...\n")
            time.sleep(2)

        else:

            print(
                f"Waiting for frame{frame_number}.jpg...",
                end="\r"
            )

            time.sleep(1)


if __name__ == "__main__":
    main()