# from ultralytics import YOLO
# import cv2
# import easyocr
# import os

# # -------------------------------
# # Load models
# # -------------------------------
# monitor_model = YOLO("models/monitor_best.pt")
# vital_model = YOLO("models/vital_best.pt")

# reader = easyocr.Reader(['en'], gpu=True)

# image_path = "images/frame.jpg"

# image = cv2.imread(image_path)

# if image is None:
#     print("Image not found!")
#     exit()

# # -------------------------------
# # Monitor Detection
# # -------------------------------
# monitor_results = monitor_model.predict(source=image, conf=0.40)

# monitor_crop = None

# for r in monitor_results:
#     for box in r.boxes:

#         x1, y1, x2, y2 = map(int, box.xyxy[0])

#         monitor_crop = image[y1:y2, x1:x2]

# if monitor_crop is None:
#     print("Monitor not detected!")
#     exit()

# os.makedirs("output", exist_ok=True)
# cv2.imwrite("output/monitor_crop.jpg", monitor_crop)

# # -------------------------------
# # Vital Detection
# # -------------------------------
# results = vital_model.predict(
#     source=monitor_crop,
#     conf=0.60,
#     iou=0.45
# )

# print("\n========== Patient Monitor ==========\n")

# class_names = vital_model.names

# for r in results:

#     for box in r.boxes:

#         x1, y1, x2, y2 = map(int, box.xyxy[0])

#         cls = int(box.cls[0])

#         label = class_names[cls]

#         crop = monitor_crop[y1:y2, x1:x2]

#         # OCR
#         text = reader.readtext(crop, detail=0)

#         value = " ".join(text)

#         print(f"{label:6} : {value}")

# print("\n====================================")

from ultralytics import YOLO
import cv2
import easyocr
import json
import os

# ----------------------------------------
# Load Models
# ----------------------------------------
monitor_model = YOLO("models/monitor_best.pt")
vital_model = YOLO("models/vital_best.pt")

# ----------------------------------------
# EasyOCR
# ----------------------------------------
reader = easyocr.Reader(['en'], gpu=True)

# ----------------------------------------
# Read Image
# ----------------------------------------
image_path = "images/frame.jpg"

image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

# ----------------------------------------
# Detect Monitor
# ----------------------------------------
monitor_results = monitor_model.predict(
    source=image,
    conf=0.45
)

monitor_crop = None

for r in monitor_results:
    for box in r.boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        monitor_crop = image[y1:y2, x1:x2]

if monitor_crop is None:
    print("Monitor not detected!")
    exit()

os.makedirs("output", exist_ok=True)

cv2.imwrite("output/monitor_crop.jpg", monitor_crop)

# ----------------------------------------
# Detect Vitals
# ----------------------------------------
vital_results = vital_model.predict(
    source=monitor_crop,
    conf=0.45,
    iou=0.45
)

class_names = vital_model.names

patient_data = {}

best_detection = {}

# ----------------------------------------
# Keep Highest Confidence Detection
# ----------------------------------------
for r in vital_results:

    for box in r.boxes:

        cls = int(box.cls[0])

        label = class_names[cls]

        conf = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if label not in best_detection:

            best_detection[label] = {
                "conf": conf,
                "box": [x1, y1, x2, y2]
            }

        else:

            if conf > best_detection[label]["conf"]:

                best_detection[label] = {
                    "conf": conf,
                    "box": [x1, y1, x2, y2]
                }

# ----------------------------------------
# OCR
# ----------------------------------------
os.makedirs("output/crops", exist_ok=True)

for label, item in best_detection.items():

    x1, y1, x2, y2 = item["box"]

    crop = monitor_crop[y1:y2, x1:x2]

    cv2.imwrite(f"output/crops/{label}.jpg", crop)

    result = reader.readtext(crop, detail=0)

    value = "".join(result).replace(" ", "")

    if value == "":
        value = "Not Detected"

    patient_data[label] = value

# ----------------------------------------
# Print Results
# ----------------------------------------
print("\n========== Patient Monitor ==========\n")

display_order = [
    "HR",
    "BP",
    "RESP",
    "SP02",
    "PULSE"
]

for key in display_order:

    value = patient_data.get(key, "Not Detected")

    print(f"{key:<6}: {value}")

print("\n====================================")

# ----------------------------------------
# Save JSON
# ----------------------------------------
with open("output/patient_data.json", "w") as f:

    json.dump(patient_data, f, indent=4)

print("\nPatient data saved to output/patient_data.json")

# from ultralytics import YOLO
# import cv2
# import easyocr
# import json
# import os

# # ----------------------------------------
# # Load Models
# # ----------------------------------------
# monitor_model = YOLO("models/monitor_best.pt")
# vital_model = YOLO("models/vital_best.pt")

# # ----------------------------------------
# # Load OCR
# # ----------------------------------------
# reader = easyocr.Reader(['en'], gpu=True)

# # ----------------------------------------
# # Read Image
# # ----------------------------------------
# image_path = "images/frame.jpg"

# image = cv2.imread(image_path)

# if image is None:
#     print("Image not found!")
#     exit()

# # ----------------------------------------
# # Detect Monitor
# # ----------------------------------------
# monitor_results = monitor_model.predict(
#     source=image,
#     conf=0.5
# )

# monitor_crop = None

# for r in monitor_results:
#     for box in r.boxes:

#         x1, y1, x2, y2 = map(int, box.xyxy[0])

#         monitor_crop = image[y1:y2, x1:x2]

# if monitor_crop is None:
#     print("Monitor not detected!")
#     exit()

# os.makedirs("output", exist_ok=True)

# cv2.imwrite("output/monitor_crop.jpg", monitor_crop)

# # ----------------------------------------
# # Detect Vital Values
# # ----------------------------------------
# vital_results = vital_model.predict(
#     source=monitor_crop,
#     conf=0.45,
#     iou=0.45
# )

# class_names = vital_model.names

# detections = {}

# # ----------------------------------------
# # Collect detections
# # ----------------------------------------
# for r in vital_results:

#     for box in r.boxes:

#         x1, y1, x2, y2 = map(int, box.xyxy[0])

#         conf = float(box.conf[0])

#         cls = int(box.cls[0])

#         label = class_names[cls]

#         detections.setdefault(label, []).append(
#             {
#                 "box":[x1,y1,x2,y2],
#                 "conf":conf
#             }
#         )

# patient_data = {}

# # ----------------------------------------
# # Merge Nearby Boxes
# # ----------------------------------------
# for label, items in detections.items():

#     items.sort(key=lambda x: x["box"][0])

#     merged = []

#     while items:

#         current = items.pop(0)

#         x1,y1,x2,y2 = current["box"]

#         changed = True

#         while changed:

#             changed = False

#             for other in items[:]:

#                 ox1,oy1,ox2,oy2 = other["box"]

#                 # merge only nearby boxes
#                 if abs(ox1-x2) < 25 and abs(oy1-y1) < 20:

#                     x1=min(x1,ox1)
#                     y1=min(y1,oy1)
#                     x2=max(x2,ox2)
#                     y2=max(y2,oy2)

#                     items.remove(other)

#                     changed=True

#         merged.append([x1,y1,x2,y2])

#     # choose best merged box
#     best_crop=None
#     best_area=0

#     for box in merged:

#         x1,y1,x2,y2=box

#         area=(x2-x1)*(y2-y1)

#         if area>best_area:

#             best_area=area

#             best_crop=monitor_crop[y1:y2,x1:x2]

#     if best_crop is None:
#         continue

#     # OCR
#     result=reader.readtext(best_crop,detail=0)

#     value="".join(result).replace(" ","")

#     if value=="":
#         value="Not detected"

#     patient_data[label]=value

# # ----------------------------------------
# # Print
# # ----------------------------------------
# print("\n========== Patient Monitor ==========\n")

# order=[
#     "HR",
#     "BP",
#     "RESP",
#     "SP02",
#     "PULSE"
# ]

# for key in order:

#     print(f"{key:<6}: {patient_data.get(key,'Not detected')}")

# print("\n====================================")

# # ----------------------------------------
# # Save JSON
# # ----------------------------------------
# with open("output/patient_data.json","w") as f:

#     json.dump(patient_data,f,indent=4)

# print("\nPatient data saved to output/patient_data.json")

# from ultralytics import YOLO
# import cv2
# import easyocr
# import json
# import os

# # ----------------------------------------
# # Load YOLO Models
# # ----------------------------------------
# monitor_model = YOLO("models/monitor_best.pt")
# vital_model = YOLO("models/vital_best.pt")

# # ----------------------------------------
# # Load EasyOCR
# # ----------------------------------------
# reader = easyocr.Reader(['en'], gpu=True)

# # ----------------------------------------
# # Read Input Image
# # ----------------------------------------
# image_path = "output\vital_detection.jpg"

# image = cv2.imread(image_path)

# if image is None:
#     print("Error: Image not found!")
#     exit()

# # ----------------------------------------
# # Detect Monitor
# # ----------------------------------------
# monitor_results = monitor_model.predict(
#     source=image,
#     conf=0.5
# )

# monitor_crop = None

# for r in monitor_results:
#     for box in r.boxes:

#         x1, y1, x2, y2 = map(int, box.xyxy[0])

#         monitor_crop = image[y1:y2, x1:x2]

# if monitor_crop is None:
#     print("Monitor not detected!")
#     exit()

# os.makedirs("output", exist_ok=True)

# cv2.imwrite("output/monitor_crop.jpg", monitor_crop)

# # ----------------------------------------
# # Detect Vital Values
# # ----------------------------------------
# vital_results = vital_model.predict(
#     source=monitor_crop,
#     conf=0.60,
#     iou=0.45
# )

# patient_data = {}

# class_names = vital_model.names

# # ----------------------------------------
# # OCR
# # ----------------------------------------
# for r in vital_results:

#     for box in r.boxes:

#         x1, y1, x2, y2 = map(int, box.xyxy[0])

#         cls = int(box.cls[0])

#         label = class_names[cls]

#         crop = monitor_crop[y1:y2, x1:x2]

#         # OCR
#         result = reader.readtext(crop, detail=0)

#         value = " ".join(result).strip()

#         patient_data[label] = value

# # ----------------------------------------
# # Print Results
# # ----------------------------------------
# print("\n========== Patient Monitor ==========\n")

# display_order = ["HR", "BP", "RESP", "SP02", "PULSE"]

# for key in display_order:
#     value = patient_data.get(key, "Not detected")
#     print(f"{key:<6}: {value}")

# print("\n====================================")

# # ----------------------------------------
# # Save JSON
# # ----------------------------------------
# with open("output/patient_data.json", "w") as file:
#     json.dump(patient_data, file, indent=4)

# print("\nPatient data saved to output/patient_data.json")