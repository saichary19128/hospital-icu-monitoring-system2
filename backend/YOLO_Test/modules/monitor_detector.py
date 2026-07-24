from ultralytics import YOLO
import cv2
import os

model = YOLO("models/monitor_best.pt")


def detect_monitor(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError("Image not found!")

    results = model.predict(
        source=image,
        conf=0.45
    )

    for r in results:

        for box in r.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            crop = image[y1:y2, x1:x2]

            # -----------------------------
            # Enlarge the entire monitor
            # -----------------------------
            crop = cv2.resize(
                crop,
                None,
                fx=3,
                fy=3,
                interpolation=cv2.INTER_CUBIC
            )

            os.makedirs("output", exist_ok=True)

            cv2.imwrite(
                "output/monitor_crop.jpg",
                crop
            )

            return crop

    return None


# from ultralytics import YOLO
# import cv2
# import os

# model = YOLO("models/monitor_best.pt")

# def detect_monitor(image_path):

#     image = cv2.imread(image_path)

#     if image is None:
#         raise FileNotFoundError("Image not found!")

#     results = model.predict(
#         source=image,
#         conf=0.45
#     )

#     for r in results:

#         for box in r.boxes:

#             x1,y1,x2,y2=map(int,box.xyxy[0])

#             crop=image[y1:y2,x1:x2]

#             os.makedirs("output",exist_ok=True)

#             cv2.imwrite(
#                 "output/monitor_crop.jpg",
#                 crop
#             )

#             return crop

#     return None