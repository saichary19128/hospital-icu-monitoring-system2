import easyocr
import cv2
import os

reader = easyocr.Reader(['en'], gpu=True)


def preprocess(crop, label):
    """
    Preprocess image before OCR.

    BP:
        - Large resize
        - CLAHE
        - Slight Gaussian blur

    Others:
        - Resize
        - Histogram Equalization
        - Otsu Threshold
    """

    if label == "BP":

        crop = cv2.resize(
            crop,
            (640, 320),
            interpolation=cv2.INTER_LANCZOS4
        )

        gray = cv2.cvtColor(
            crop,
            cv2.COLOR_BGR2GRAY
        )

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        gray = clahe.apply(gray)

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        return gray

    else:

        crop = cv2.resize(
            crop,
            (160, 160),
            interpolation=cv2.INTER_CUBIC
        )

        gray = cv2.cvtColor(
            crop,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.equalizeHist(gray)

        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        return thresh


def read_values(best_detection, monitor_crop):

    patient_data = {}

    os.makedirs(
        "output/crops",
        exist_ok=True
    )

    print("\n========== OCR Results ==========\n")

    for label, item in best_detection.items():

        x1, y1, x2, y2 = item["box"]

        # -------------------------------------------------
        # Crop adjustment
        # -------------------------------------------------

        if label == "BP":

            # Larger horizontal padding helps OCR read
            # the complete BP value (e.g. 122/83)

            padding_x = 25
            padding_y = 8

            x1 = max(0, x1 - padding_x)
            y1 = max(0, y1 - padding_y)

            x2 = min(monitor_crop.shape[1], x2 + padding_x)
            y2 = min(monitor_crop.shape[0], y2 + padding_y)

        else:

            if label == "HR":
                x1 += 3

            elif label == "RESP":
                x1 += 3

            elif label == "SP02":
                x1 += 3

            elif label == "PULSE":
                x1 += 3

            x1 = max(0, x1)
            x2 = min(monitor_crop.shape[1], x2)

        original_crop = monitor_crop[y1:y2, x1:x2]

        # Save original BP crop

        if label == "BP":

            cv2.imwrite(
                "output/crops/BP_original.jpg",
                original_crop
            )

        crop = preprocess(
            original_crop,
            label
        )

        # Save processed BP crop

        if label == "BP":

            cv2.imwrite(
                "output/crops/BP_processed.jpg",
                crop
            )

        cv2.imwrite(
            f"output/crops/{label}.jpg",
            crop
        )

        result = reader.readtext(
            crop,
            detail=1,
            paragraph=False,
            allowlist="0123456789./"
        )

        print(
            f"{label:<6} Raw OCR -> {result}"
        )

        # -----------------------------------------
        # Select OCR result with HIGHEST confidence
        # -----------------------------------------

        if len(result) > 0:

            best = max(result, key=lambda x: x[2])

            value = best[1].replace(" ", "")

            confidence = best[2]

            print(
                f"{label:<6} Confidence -> {confidence:.2f}"
            )

            # -----------------------------------------
            # Remove MAP value for BP
            #
            # 106/82/913  -> 106/82
            # 120/80      -> 120/80
            # 70/44       -> 70/44
            # -----------------------------------------

            if label == "BP":

                parts = value.split("/")

                if len(parts) >= 2:

                    value = f"{parts[0]}/{parts[1]}"

        else:

            value = "Not Detected"

        patient_data[label] = value

    print("\n===============================\n")

    return patient_data



# import easyocr
# import cv2
# import os

# reader = easyocr.Reader(['en'], gpu=True)


# def preprocess(crop, label):
#     """
#     Preprocess image before OCR.
#     BP uses grayscale + CLAHE.
#     Other vitals use Otsu threshold.
#     """

#     if label == "BP":

#         crop = cv2.resize(
#             crop,
#             (640, 320),
#             interpolation=cv2.INTER_LANCZOS4
#         )

#         gray = cv2.cvtColor(
#             crop,
#             cv2.COLOR_BGR2GRAY
#         )

#         clahe = cv2.createCLAHE(
#             clipLimit=2.0,
#             tileGridSize=(8, 8)
#         )

#         gray = clahe.apply(gray)

#         gray = cv2.GaussianBlur(
#             gray,
#             (3, 3),
#             0
#         )

#         return gray

#     else:

#         crop = cv2.resize(
#             crop,
#             (160, 160),
#             interpolation=cv2.INTER_CUBIC
#         )

#         gray = cv2.cvtColor(
#             crop,
#             cv2.COLOR_BGR2GRAY
#         )

#         gray = cv2.equalizeHist(gray)

#         _, thresh = cv2.threshold(
#             gray,
#             0,
#             255,
#             cv2.THRESH_BINARY + cv2.THRESH_OTSU
#         )

#         return thresh


# def read_values(best_detection, monitor_crop):

#     patient_data = {}

#     os.makedirs(
#         "output/crops",
#         exist_ok=True
#     )

#     print("\n========== OCR Results ==========\n")

#     for label, item in best_detection.items():

#         x1, y1, x2, y2 = item["box"]

#         # -----------------------------------
#         # Crop adjustment
#         # -----------------------------------

#         if label == "BP":

#             padding = 8

#             x1 = max(0, x1 - padding)
#             y1 = max(0, y1 - padding)

#             x2 = min(monitor_crop.shape[1], x2 + padding)
#             y2 = min(monitor_crop.shape[0], y2 + padding)

#         else:

#             if label == "HR":
#                 x1 += 3

#             elif label == "RESP":
#                 x1 += 3

#             elif label == "SP02":
#                 x1 += 3

#             elif label == "PULSE":
#                 x1 += 3

#             x1 = max(0, x1)
#             x2 = min(monitor_crop.shape[1], x2)

#         original_crop = monitor_crop[y1:y2, x1:x2]

#         if label == "BP":

#             cv2.imwrite(
#                 "output/crops/BP_original.jpg",
#                 original_crop
#             )

#         crop = preprocess(
#             original_crop,
#             label
#         )

#         if label == "BP":

#             cv2.imwrite(
#                 "output/crops/BP_processed.jpg",
#                 crop
#             )

#         cv2.imwrite(
#             f"output/crops/{label}.jpg",
#             crop
#         )

#         result = reader.readtext(
#             crop,
#             detail=1,
#             paragraph=False,
#             allowlist="0123456789./"
#         )

#         print(
#             f"{label:<6} Raw OCR -> {result}"
#         )

#         if len(result) > 0:
#             value = result[0][1].replace(" ", "")
#             confidence = result[0][2]

#             print(
#                 f"{label:<6} Confidence -> {confidence:.2f}"
#             )

#         else:
#             value = "Not Detected"

#         patient_data[label] = value

#     print("\n===============================\n")

#     return patient_data




# import easyocr
# import cv2
# import os

# reader = easyocr.Reader(['en'], gpu=True)


# def preprocess(crop, label):
#     """
#     Preprocess image before OCR.
#     BP uses grayscale + CLAHE only.
#     Other vitals use Otsu threshold.
#     """

#     if label == "BP":

#         crop = cv2.resize(
#             crop,
#             (640, 320),
#             interpolation=cv2.INTER_LANCZOS4
#         )

#         gray = cv2.cvtColor(
#             crop,
#             cv2.COLOR_BGR2GRAY
#         )

#         # Better local contrast enhancement
#         clahe = cv2.createCLAHE(
#             clipLimit=2.0,
#             tileGridSize=(8, 8)
#         )

#         gray = clahe.apply(gray)

#         # Small blur removes tiny noise while preserving edges
#         gray = cv2.GaussianBlur(
#             gray,
#             (3, 3),
#             0
#         )

#         return gray

#     else:

#         crop = cv2.resize(
#             crop,
#             (160, 160),
#             interpolation=cv2.INTER_CUBIC
#         )

#         gray = cv2.cvtColor(
#             crop,
#             cv2.COLOR_BGR2GRAY
#         )

#         gray = cv2.equalizeHist(gray)

#         _, thresh = cv2.threshold(
#             gray,
#             0,
#             255,
#             cv2.THRESH_BINARY + cv2.THRESH_OTSU
#         )

#         return thresh


# def read_values(best_detection, monitor_crop):

#     patient_data = {}

#     os.makedirs(
#         "output/crops",
#         exist_ok=True
#     )

#     print("\n========== OCR Results ==========\n")

#     for label, item in best_detection.items():

#         x1, y1, x2, y2 = item["box"]

#         # -----------------------------
#         # Crop adjustments
#         # -----------------------------

#         if label == "BP":
#             x1 += 2

#         elif label == "HR":
#             x1 += 3

#         elif label == "RESP":
#             x1 += 3

#         elif label == "SP02":
#             x1 += 3

#         elif label == "PULSE":
#             x1 += 3

#         x1 = max(0, x1)
#         x2 = min(monitor_crop.shape[1], x2)

#         original_crop = monitor_crop[y1:y2, x1:x2]

#         # Save original BP crop
#         if label == "BP":
#             cv2.imwrite(
#                 "output/crops/BP_original.jpg",
#                 original_crop
#             )

#         crop = preprocess(
#             original_crop,
#             label
#         )

#         # Save processed BP crop
#         if label == "BP":
#             cv2.imwrite(
#                 "output/crops/BP_processed.jpg",
#                 crop
#             )

#         cv2.imwrite(
#             f"output/crops/{label}.jpg",
#             crop
#         )

#         result = reader.readtext(
#             crop,
#             detail=0,
#             paragraph=False,
#             allowlist="0123456789./"
#         )

#         print(
#             f"{label:<6} Raw OCR -> {result}"
#         )

#         value = "".join(result).replace(
#             " ",
#             ""
#         )

#         if value == "":
#             value = "Not Detected"

#         patient_data[label] = value

#     print("\n===============================\n")

#     return patient_data



# import easyocr
# import cv2
# import os

# reader=easyocr.Reader(['en'],gpu=True)

# def read_values(best_detection,monitor_crop):

#     patient_data={}

#     os.makedirs("output/crops",exist_ok=True)

#     for label,item in best_detection.items():

#         x1,y1,x2,y2=item["box"]

#         crop=monitor_crop[y1:y2,x1:x2]

#         cv2.imwrite(

#             f"output/crops/{label}.jpg",

#             crop

#         )

#         result=reader.readtext(

#             crop,

#             detail=0

#         )

#         value="".join(result).replace(" ","")

#         if value=="":

#             value="Not Detected"

#         patient_data[label]=value

#     return patient_data