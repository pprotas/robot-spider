import cv2
import numpy as np
import math


def main():
    video = cv2.VideoCapture(0)

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        for i in range(len(contours)):
            #c = contours[i]

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            blue_lower = np.array([100, 150, 0], np.uint8)
            blue_upper = np.array([140, 255, 255], np.uint8)
            mask = cv2.inRange(hsv, blue_lower, blue_upper)
            contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

            if len(contours) > 0:
                try:
                    frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
                except:
                    print("no black")

                cv2.imshow("mask", mask)
                cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #video.release()
        #cv2.destroyAllWindows()


if __name__ == "__main__":
    main()