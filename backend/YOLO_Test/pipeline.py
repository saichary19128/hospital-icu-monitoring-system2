from modules.monitor_detector import detect_monitor
from modules.vital_detector import detect_vitals
from modules.ocr_reader import read_values
from modules.utils import print_patient

import time


def run_pipeline(image_path):
    """
    Runs the complete ICU monitor pipeline.

    Args:
        image_path (str): Path to the monitor image.

    Returns:
        dict | None:
            Returns patient data dictionary if monitor detected.
            Returns None if monitor is not detected.
    """

    total_start = time.perf_counter()

    # ----------------------------
    # Monitor Detection
    # ----------------------------
    start = time.perf_counter()

    monitor_crop = detect_monitor(image_path)

    monitor_time = time.perf_counter() - start

    if monitor_crop is None:
        print("Monitor not detected!")
        return None

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

    total_time = time.perf_counter() - total_start

    # ----------------------------
    # Performance (Console Only)
    # ----------------------------
    print("\n========== Performance ==========\n")

    print(f"Monitor Detection : {monitor_time:.3f} sec")
    print(f"Vital Detection   : {vital_time:.3f} sec")
    print(f"OCR               : {ocr_time:.3f} sec")

    print("---------------------------------")
    print(f"Total Time        : {total_time:.3f} sec")

    print("\n=================================\n")

    return patient


def main():

    image = "images/frame.jpg"

    patient = run_pipeline(image)

    if patient is None:
        return

    print_patient(patient)


if __name__ == "__main__":
    main()

# from modules.monitor_detector import detect_monitor
# from modules.vital_detector import detect_vitals
# from modules.ocr_reader import read_values
# from modules.json_writer import save_json
# from modules.utils import print_patient

# import time


# def main():

#     total_start = time.perf_counter()

#     image = "images/frame.jpg"

#     # ----------------------------
#     # Monitor Detection
#     # ----------------------------
#     start = time.perf_counter()

#     monitor_crop = detect_monitor(image)

#     monitor_time = time.perf_counter() - start

#     if monitor_crop is None:
#         print("Monitor not detected!")
#         return

#     # ----------------------------
#     # Vital Detection
#     # ----------------------------
#     start = time.perf_counter()

#     detections = detect_vitals(monitor_crop)

#     vital_time = time.perf_counter() - start

#     # ----------------------------
#     # OCR
#     # ----------------------------
#     start = time.perf_counter()

#     patient = read_values(
#         detections,
#         monitor_crop
#     )

#     ocr_time = time.perf_counter() - start

#     # ----------------------------
#     # Print Results
#     # ----------------------------
#     print_patient(patient)

#     # ----------------------------
#     # Save JSON
#     # ----------------------------
#     start = time.perf_counter()

#     save_json(patient)

#     json_time = time.perf_counter() - start

#     total_time = time.perf_counter() - total_start

#     print("\nPatient data saved to output/patient_data.json")

#     print("\n========== Performance ==========\n")

#     print(f"Monitor Detection : {monitor_time:.3f} sec")
#     print(f"Vital Detection   : {vital_time:.3f} sec")
#     print(f"OCR               : {ocr_time:.3f} sec")
#     print(f"JSON Save         : {json_time:.3f} sec")

#     print("---------------------------------")
#     print(f"Total Time        : {total_time:.3f} sec")

#     print("\n=================================")


# if __name__ == "__main__":
#     main()




# from modules.monitor_detector import detect_monitor

# from modules.vital_detector import detect_vitals

# from modules.ocr_reader import read_values

# from modules.json_writer import save_json

# from modules.utils import print_patient


# def main():

#     image="images/frame.jpg"

#     monitor_crop=detect_monitor(image)

#     if monitor_crop is None:

#         print("Monitor not detected!")

#         return

#     detections=detect_vitals(monitor_crop)

#     patient=read_values(

#         detections,

#         monitor_crop

#     )

#     print_patient(patient)

#     save_json(patient)

#     print(

#         "\nPatient data saved to output/patient_data.json"

#     )


# if __name__=="__main__":

#     main()