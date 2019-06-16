import argparse
import datetime
import imutils
import math
import cv2
import numpy as np

textIn = 0
textOut = 0

def testIntersectionIn(y_rec, y_blueline):
    if (y_rec == y_blueline):
        print("Entrou siow")
        return True
    return False


if __name__ == "__main__":
    camera = cv2.VideoCapture("camerasuperior2.wmv")

    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    firstFrame = None

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 12000:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            y_blueline = height // 2

            y_redline = y_blueline - 30

            cv2.line(frame, (0, y_blueline), (width, y_blueline), (250, 0, 1), 2)
            #cv2.line(frame, (0, y_redline), (width, y_redline), (0, 0, 255), 2)

            x_rectangle = (x + x + w) // 2
            y_rectangle = (y + y + h) // 2

            rectagleCenterPont = (x_rectangle, y_rectangle)
            cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)

            if (testIntersectionIn(y_rectangle, y_blueline)):
                textIn += 1

			# if (testIntersectionOut((x + x + w) // 2, (y + y + h) // 2)):
			# 	textOut += 1

            # draw the text and timestamp on the frame

            # show the frame and record if the user presses a key
            #cv2.imshow("Thresh", thresh)
            #cv2.imshow("Frame Delta", frameDelta)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.putText(frame, "In: {}".format(str(textIn)), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		#cv2.putText(frame, "Out: {}".format(str(textOut)), (10, 70),
		#cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
