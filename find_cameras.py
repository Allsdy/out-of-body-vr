import cv2

print("Scanning for cameras (Indices 0-4)...")

# Check first 5 indexes
for index in range(5):
    cap = cv2.VideoCapture(index)
    
    if cap.isOpened():
        # Try to read a frame
        ret, frame = cap.read()
        if ret:
            filename = f"camera_index_{index}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✅ Camera Index {index}: OPEN. Saved photo as '{filename}'")
        else:
            print(f"⚠️  Camera Index {index}: Open, but returned empty/black frame.")
        cap.release()
    else:
        print(f"❌ Camera Index {index}: Not found.")
        