from ultralytics import YOLO
import cv2
import os

model = YOLO("models/monitor_best.pt")

image_path = "images/frame.jpg"

image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

print("Image loaded successfully!")

results = model.predict(source=image, conf=0.25)

os.makedirs("output", exist_ok=True)

for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        crop = image[y1:y2, x1:x2]

        cv2.imwrite("output/monitor_crop.jpg", crop)

        print("Monitor detected!")

print("Done")