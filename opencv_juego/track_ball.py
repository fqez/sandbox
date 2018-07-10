import cv2
import numpy
import math

GREEN_MIN = numpy.array([20, 50, 100],numpy.uint8)#numpy.array([48, 138, 138],numpy.uint8)
GREEN_MAX = numpy.array([90, 235, 210],numpy.uint8)#numpy.array([67, 177, 192],numpy.uint8)

BLUE_MIN = numpy.array([108, 176, 48],numpy.uint8)#numpy.array([104, 200, 42],numpy.uint8)
BLUE_MAX = numpy.array([179, 255, 255],numpy.uint8)#numpy.array([179, 255, 255],numpy.uint8)

RED_MIN = numpy.array([163, 209, 30],numpy.uint8)#numpy.array([48, 138, 138],numpy.uint8)
RED_MAX = numpy.array([179, 255, 255],numpy.uint8)#numpy.array([67, 177, 192],numpy.uint8)

centers = []


def locateBall(lower, upper, flag):
    # convert to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # construct a mask for the color specified
    # then perform a series of dilations and erosions
    # to remove any small blobs left in the mask
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and
    # initialize the current center
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle border
            cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 2)

            # and the centroid
            cv2.circle(image, center, 5, (0, 255, 255), -1)

            
            centers.append(center)
        
        if len(centers) > 1:
            cv2.line(image, centers[0], centers[1], (255,0,0), 3)
            dist = math.sqrt( (centers[1][0] - centers[0][0])**2 + (centers[1][1] - centers[0][1])**2 )
            x = int((centers[0][0] + centers[1][0] )/ 2)
            y = int((centers[1][0] + centers[1][1] )/ 2)
            cv2.putText(image, str(int(dist)),  (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow("ball"+flag, mask)        
    


cap = cv2.VideoCapture(0)

while cap.isOpened():

    centers = []
    ret, image = cap.read()
    # resize the image
    #image = dameImagen()
    #locateBall(BLUE_MIN, BLUE_MAX,"a")
    locateBall(RED_MIN, RED_MAX, "r")
    print(centers)
    cv2.imshow("orig", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):        # exit when 'q' pressed
        break


cap.release()
cv2.destroyAllWindows()