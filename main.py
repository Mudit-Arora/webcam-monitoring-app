import cv2
# collaborate with numpy library
import time

# main camera
video = cv2.VideoCapture(0)
time.sleep(1)

while True:
    check, frame = video.read()
    # processes video
    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)
    # camera turns off when q key is pressed
    if key == ord("q"):
        break

# shows your video using camera
video.release()

