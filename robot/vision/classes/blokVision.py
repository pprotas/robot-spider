import cv2
import numpy as np
import math


def main():
    video = cv2.VideoCapture(0)

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_NONE)

        blokArea = 0
        blok = None
        roi = None
        x, y, w, h = "", "", "", ""

        for i in range(len(contours)):
            c = contours[i]
            x, y, w, h = cv2.boundingRect(c)
            roi = frame[y:y + h, x:x + w]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            blue_lower = np.array([100, 150, 0])
            blue_upper = np.array([140, 255, 255])
            mask = cv2.inRange(hsv, blue_lower, blue_upper)
            blueContours, blueHierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

            try:
                # frame = cv2.drawContours(frame, blueContours, -1, (0, 255, 0), 3)
                update = False
                for j in range(len(blueContours)):
                    bc = blueContours[j]
                    area = cv2.contourArea(bc)
                    if (area > blokArea):
                        blokArea = area
                        blok = bc
                        update = True
                    if update:
                        roi = cv2.drawContours(roi, [blok], 0, (0, 255, 0), 3)

            except:
                print("no black")

        frame[y:y + h, x:x + w] = roi
        # cv2.imshow("img", roi)
        cv2.imshow("mask", thresh)
        cv2.imshow("frame", frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #video.release()
        #cv2.destroyAllWindows()


if __name__ == "__main__":
    main()