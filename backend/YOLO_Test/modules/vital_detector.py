from ultralytics import YOLO
import cv2
import os

# Load both models
model1 = YOLO("models/vital_model1.pt")
model2 = YOLO("models/vital_model2.pt")


def run_model(model, model_name, monitor_crop):

    results = model.predict(
        source=monitor_crop,
        conf=0.20,
        iou=0.45
    )

    class_names = model.names

    detections = {}

    for r in results:

        for box in r.boxes:

            cls = int(box.cls[0])
            label = class_names[cls]
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            width = x2 - x1
            height = y2 - y1
            area = width * height

            if label not in detections or conf > detections[label]["conf"]:

                detections[label] = {
                    "conf": conf,
                    "box": [x1, y1, x2, y2],
                    "width": width,
                    "height": height,
                    "area": area,
                    "model": model_name
                }

    return detections


def merge_detections(d1, d2):

    final = {}

    labels = ["HR", "BP", "RESP", "SP02", "PULSE"]

    for label in labels:

        if label in d1 and label in d2:

            # Keep the detection with higher confidence
            if d1[label]["conf"] >= d2[label]["conf"]:
                final[label] = d1[label]
            else:
                final[label] = d2[label]

        elif label in d1:

            final[label] = d1[label]

        elif label in d2:

            final[label] = d2[label]

    return final


def detect_vitals(monitor_crop):

    detections1 = run_model(
        model1,
        "Model 1",
        monitor_crop
    )

    detections2 = run_model(
        model2,
        "Model 2",
        monitor_crop
    )

    best_detection = merge_detections(
        detections1,
        detections2
    )

    annotated = monitor_crop.copy()

    os.makedirs("output/crops", exist_ok=True)

    print("\n========== Merged Detection Results ==========\n")

    for label, item in best_detection.items():

        x1, y1, x2, y2 = item["box"]

        cv2.rectangle(
            annotated,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            annotated,
            label,
            (x1, y1 - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        print(
            f"{label:<6} -> "
            f"{item['model']} | "
            f"Conf: {item['conf']:.2%} | "
            f"Size: {item['width']}x{item['height']}"
        )

    cv2.imwrite(
        "output/vital_detection.jpg",
        annotated
    )

    print("\n==============================================")

    return best_detection

# from ultralytics import YOLO
# import cv2
# import os

# # Load both models
# model1 = YOLO("models/vital_model1.pt")
# model2 = YOLO("models/vital_model2.pt")


# def run_model(model, model_name, monitor_crop):

#     results = model.predict(
#         source=monitor_crop,
#         conf=0.20,
#         iou=0.45
#     )

#     class_names = model.names

#     detections = {}

#     for r in results:

#         for box in r.boxes:

#             cls = int(box.cls[0])
#             label = class_names[cls]
#             conf = float(box.conf[0])

#             x1, y1, x2, y2 = map(int, box.xyxy[0])

#             if label not in detections or conf > detections[label]["conf"]:

#                 detections[label] = {
#                     "conf": conf,
#                     "box": [x1, y1, x2, y2],
#                     "model": model_name
#                 }

#     return detections


# def merge_detections(d1, d2):

#     final = {}

#     labels = ["HR", "BP", "RESP", "SP02", "PULSE"]

#     for label in labels:

#         if label in d1 and label in d2:

#             if d1[label]["conf"] >= d2[label]["conf"]:
#                 final[label] = d1[label]
#             else:
#                 final[label] = d2[label]

#         elif label in d1:

#             final[label] = d1[label]

#         elif label in d2:

#             final[label] = d2[label]

#     return final


# def detect_vitals(monitor_crop):

#     detections1 = run_model(
#         model1,
#         "Model 1",
#         monitor_crop
#     )

#     detections2 = run_model(
#         model2,
#         "Model 2",
#         monitor_crop
#     )

#     best_detection = merge_detections(
#         detections1,
#         detections2
#     )

#     annotated = monitor_crop.copy()

#     os.makedirs("output/crops", exist_ok=True)

#     print("\n========== Merged Detection Results ==========\n")

#     for label, item in best_detection.items():

#         x1, y1, x2, y2 = item["box"]

#         cv2.rectangle(
#             annotated,
#             (x1, y1),
#             (x2, y2),
#             (0, 255, 0),
#             2
#         )

#         cv2.putText(
#             annotated,
#             label,
#             (x1, y1 - 8),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.6,
#             (0, 255, 0),
#             2
#         )

#         print(
#             f"{label:<6} -> {item['model']} ({item['conf']:.2%})"
#         )

#     cv2.imwrite(
#         "output/vital_detection.jpg",
#         annotated
#     )

#     print("\n==============================================")

#     return best_detection



# # from ultralytics import YOLO
# # import cv2
# # import os

# # model=YOLO("models/vital_best.pt")


# # def detect_vitals(monitor_crop):

# #     results=model.predict(

# #         source=monitor_crop,

# #         conf=0.45,

# #         iou=0.45

# #     )

# #     annotated=monitor_crop.copy()

# #     class_names=model.names

# #     best_detection={}

# #     os.makedirs("output/crops",exist_ok=True)

# #     for r in results:

# #         for i,box in enumerate(r.boxes):

# #             cls=int(box.cls[0])

# #             label=class_names[cls]

# #             conf=float(box.conf[0])

# #             x1,y1,x2,y2=map(int,box.xyxy[0])

# #             if label not in best_detection:

# #                 best_detection[label]={

# #                     "conf":conf,

# #                     "box":[x1,y1,x2,y2]

# #                 }

# #             elif conf>best_detection[label]["conf"]:

# #                 best_detection[label]={

# #                     "conf":conf,

# #                     "box":[x1,y1,x2,y2]

# #                 }

# #             cv2.rectangle(

# #                 annotated,

# #                 (x1,y1),

# #                 (x2,y2),

# #                 (0,255,0),

# #                 2

# #             )

# #             cv2.putText(

# #                 annotated,

# #                 f"{label} {conf:.2f}",

# #                 (x1,y1-8),

# #                 cv2.FONT_HERSHEY_SIMPLEX,

# #                 0.6,

# #                 (0,255,0),

# #                 2

# #             )

# #     cv2.imwrite(

# #         "output/vital_detection.jpg",

# #         annotated

# #     )

# #     return best_detection

# from ultralytics import YOLO
# import cv2
# import os

# # Load both models
# model1 = YOLO("models/vital_model1.pt")
# model2 = YOLO("models/vital_model2.pt")


# def run_model(model, monitor_crop):

#     results = model.predict(
#         source=monitor_crop,
#         conf=0.45,
#         iou=0.45
#     )

#     class_names = model.names

#     detections = {}

#     for r in results:

#         for box in r.boxes:

#             cls = int(box.cls[0])
#             label = class_names[cls]
#             conf = float(box.conf[0])

#             x1, y1, x2, y2 = map(int, box.xyxy[0])

#             if (
#                 label not in detections
#                 or
#                 conf > detections[label]["conf"]
#             ):

#                 detections[label] = {
#                     "conf": conf,
#                     "box": [x1, y1, x2, y2]
#                 }

#     return detections


# def merge_detections(d1, d2):

#     final = {}

#     labels = ["HR", "BP", "RESP", "SP02", "PULSE"]

#     for label in labels:

#         if label in d1 and label in d2:

#             if d1[label]["conf"] >= d2[label]["conf"]:
#                 final[label] = d1[label]
#             else:
#                 final[label] = d2[label]

#         elif label in d1:

#             final[label] = d1[label]

#         elif label in d2:

#             final[label] = d2[label]

#     return final


# def detect_vitals(monitor_crop):

#     # Run both models
#     detections1 = run_model(model1, monitor_crop)
#     detections2 = run_model(model2, monitor_crop)

#     # Merge detections
#     best_detection = merge_detections(detections1, detections2)

#     # Draw merged detections
#     annotated = monitor_crop.copy()

#     os.makedirs("output/crops", exist_ok=True)

#     for label, item in best_detection.items():

#         x1, y1, x2, y2 = item["box"]

#         cv2.rectangle(
#             annotated,
#             (x1, y1),
#             (x2, y2),
#             (0, 255, 0),
#             2
#         )

#         cv2.putText(
#             annotated,
#             label,
#             (x1, y1 - 8),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.6,
#             (0, 255, 0),
#             2
#         )

#     cv2.imwrite("output/vital_detection.jpg", annotated)

#     return best_detection