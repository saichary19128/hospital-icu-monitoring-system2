from ultralytics import YOLO
import cv2
import os

model = YOLO("models/monitor_best.pt")


def detect_monitor(frame):
    """
    Detect ICU monitor from an OpenCV frame.
    Returns cropped monitor image.
    """

    if frame is None:
        return None

    results = model.predict(
        source=frame,
        conf=0.45,
        verbose=False
    )

    for r in results:

        for box in r.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            crop = frame[y1:y2, x1:x2]

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


def detect_monitor_from_image(image_path):
    """
    Compatibility wrapper.
    Allows existing image-based code to continue working.
    """

    frame = cv2.imread(image_path)

    if frame is None:
        raise FileNotFoundError(image_path)

    return detect_monitor(frame)