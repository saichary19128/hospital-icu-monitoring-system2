from ultralytics import YOLO
import cv2
import os

# Load vital detection model
model = YOLO("models/vital_best.pt")

# Load cropped monitor image
image_path = "output/monitor_crop.jpg"
# image_path = "images/frame.jpg"
image = cv2.imread(image_path)

if image is None:
    print("Error: monitor_crop.jpg not found!")
    exit()

# Run inference
results = model.predict(source=image, conf=0.45, iou=0.45)

annotated = image.copy()

class_names = model.names

# Create crops folder
os.makedirs("output/crops", exist_ok=True)

print("\nDetected Objects\n")

for r in results:

    for i, box in enumerate(r.boxes):

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cls = int(box.cls[0])
        conf = float(box.conf[0])

        label = class_names[cls]

        print(f"{label:8}  Confidence: {conf:.2%}")

        # Draw rectangle
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0,255,0), 2)

        cv2.putText(
            annotated,
            f"{label} {conf:.2f}",
            (x1, y1-8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

        # Save crop
        crop = image[y1:y2, x1:x2]

        cv2.imwrite(f"output/crops/{label}_{i}.jpg", crop)

# Save annotated image
cv2.imwrite("output/vital_detection.jpg", annotated)

print("\nFinished Successfully!")