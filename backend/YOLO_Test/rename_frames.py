import os

folder = "frames"

# Get all image files
files = [
    f for f in os.listdir(folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

# Sort for consistent ordering
files.sort()

# Step 1: Rename temporarily to avoid filename conflicts
for i, file in enumerate(files):
    old_path = os.path.join(folder, file)
    temp_path = os.path.join(folder, f"temp_{i}.jpg")
    os.rename(old_path, temp_path)

# Step 2: Rename to frame1, frame2, ...
temp_files = sorted(
    [f for f in os.listdir(folder) if f.startswith("temp_")]
)

for i, file in enumerate(temp_files, start=1):
    old_path = os.path.join(folder, file)
    new_path = os.path.join(folder, f"frame{i}.jpg")
    os.rename(old_path, new_path)

print(f"Successfully renamed {len(temp_files)} images.")