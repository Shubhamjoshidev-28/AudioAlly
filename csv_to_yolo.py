import pandas as pd
import os

# -------- PATHS --------
CSV_PATH = r"D:\archive\valid\_annotations.csv"
IMAGES_DIR = "E:\AudioAlly\dataset\set\images"
LABELS_DIR = "E:\AudioAlly\dataset\set\labels"

os.makedirs(LABELS_DIR, exist_ok=True)

# -------- LOAD CSV --------
df = pd.read_csv(CSV_PATH)

# -------- CLASS MAP --------
CLASS_MAP = {"person": 0}

# -------- PROCESS --------
for _, row in df.iterrows():
    filename = row["filename"]
    img_w = row["width"]
    img_h = row["height"]
    class_name = row["class"]

    xmin = row["xmin"]
    ymin = row["ymin"]
    xmax = row["xmax"]
    ymax = row["ymax"]

    # Safety check
    if class_name not in CLASS_MAP:
        continue

    # YOLO conversion
    x_center = ((xmin + xmax) / 2) / img_w
    y_center = ((ymin + ymax) / 2) / img_h
    box_width = (xmax - xmin) / img_w
    box_height = (ymax - ymin) / img_h

    class_id = CLASS_MAP[class_name]

    label_file = os.path.join(
        LABELS_DIR,
        os.path.splitext(filename)[0] + ".txt"
    )

    with open(label_file, "a") as f:
        f.write(
            f"{class_id} {x_center:.6f} {y_center:.6f} "
            f"{box_width:.6f} {box_height:.6f}\n"
        )

print("✅ Excel/CSV annotations successfully converted to YOLO format")
