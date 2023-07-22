import cv2
# collaborate with numpy library
import time
from emailing import send_email
import glob  # module to return specific file path
import os
from threading import Thread

# main camera
video = cv2.VideoCapture(0)
time.sleep(1)

# making first frame (original)
first_frame = None
status_list = []
count = 1

# function to remove all the previous images from the folder after running the program
def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

# iterations until program breaks
while True:
    status = 0 # when there is no object in frame
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
        # checking if there is an object in the area
        if cv2.contourArea(contour) < 2000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        # making a rectangle of green color around the object
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1 # when there is object in frame
            # saving image at 30fps
            cv2.imwrite(f"images/image{count}.png", frame)
            count = count + 1  # iterating after every loop
            # choosing the middle image
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:] # last two items from the list

    # checking if the object has left the frame or not
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        # send_email(image_with_object)
        clean_thread = Thread(target=clean_folder)
        email_thread.daemon = True
        # clean_folder()
        email_thread.start()
        clean_thread.start()

    print(status_list)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    # camera turns off when q key is pressed
    if key == ord("q"):
        break

# shows your video using camera
video.release()

