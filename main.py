import cv2
# collaborate with numpy library
import time

# main camera
video = cv2.VideoCapture(0)
check, frame = video.read()
time.sleep(1)

print(check)
print(frame)