import os
from dotenv import load_dotenv
import cv2

video = cv2.VideoCapture(0)

load_dotenv()
path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), "datasets-face-recognition")

facedetect = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

face_id = input("Enter Your ID: ")
face_id = int(face_id)
count = 0

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        count = count+1
        cv2.imwrite(
            # str(os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), "datasets-face-recognition"))
            path
            + '/User.' + str(face_id) + "." + str(count) + ".jpg", gray[y:y + h, x:x + w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)

    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1)

    if count > 200:
        break

video.release()
cv2.destroyAllWindows()
print("Dataset Collection Done..................")
