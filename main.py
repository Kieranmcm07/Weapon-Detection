import numpy as np
import cv2
import imutils
import datetime

# Load the cascade classifier
gun_cascade = cv2.CascadeClassifier("cascade.xml")

# Check if the classifier is loaded correctly
if not gun_cascade:
    print("Error loading cascade classifier")
    exit()

# Open the camera
camera = cv2.VideoCapture(0)

gun_exist = False

while True:
    # Read a frame from the camera
    ret, frame = camera.read()

    # Check if the frame is not empty
    if not ret:
        print("Error reading frame from camera")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect guns in the grayscale image
    gun = gun_cascade.detectMultiScale(gray, 1.3, 5)

    # Check if any guns were detected
    if len(gun) > 0:
        gun_exist = True
    else:
        gun_exist = False

    for (x, y, w, h) in gun:
        if gun_exist:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red box
        else:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

    if gun_exist:
        cv2.putText(frame, "WEAPON DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "NO WEAPON DETECTED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()