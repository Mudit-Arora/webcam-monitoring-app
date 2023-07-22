import cv2
# collaborate with numpy library
import time

# main camera
video = cv2.VideoCapture(0)
time.sleep(1)

# making first frame (original)
first_frame = None

# iterations until program breaks
while True:
    check, frame = video.read() # matrix
    # checking to gray frame to reduce data
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # making video a bit blurry to increase the efficiency
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # only true for first iteration, gray frame becomes original frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # comparing the first frame and current frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # changing the pixels using threshold function
    thres_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    # removing noise from background
    dil_frame = cv2.dilate(thres_frame, None, iterations=2)
    # processes video
    cv2.imshow("My video", dil_frame)

    # checking for contours 
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 2000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        # making a rectangle of green color around the object
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    # camera turns off when q key is pressed
    if key == ord("q"):
        break

# shows your video using camera
video.release()

