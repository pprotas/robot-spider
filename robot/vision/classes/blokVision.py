import cv2
import numpy as np
import math

def main():
    video = cv2.VideoCapture(0)
    width = video.get(3)
    height = video.get(4)
    centerX = width/2;
    centerY = height/2;

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_NONE)
        # hsvWit = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # wit_lower = np.array([0, 0, 0])
        # wit_higher = np.array([0, 0, 255])
        # mask_wit = cv2.inRange(hsvWit, wit_lower, wit_higher)
        # res = cv2.bitwise_and(frame, frame, mask=mask_wit)
        # contours, hierarchy = cv2.findContours(mask_wit, 1, cv2.CHAIN_APPROX_NONE)
        # contours = []

        blokArea = 0
        blok = None
        roi = None
        superRoi = None
        superBlok = None
        x, y, w, h = "", "", "", ""

        for i in range(len(contours)):
            c = contours[i]
            x, y, w, h = cv2.boundingRect(c)
            roi = frame[y:y + h, x:x + w]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            blue_lower = np.array([100, 150, 0])
            blue_higher = np.array([140, 255, 255])
            mask = cv2.inRange(hsv, blue_lower, blue_higher)
            blueContours, blueHierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

            try:
                update = False
                for j in range(len(blueContours)):
                    bc = blueContours[j]
                    area = cv2.contourArea(bc)
                    if (area > blokArea):
                        blokArea = area
                        blok = bc
                        update = True
                    if update:
                        superRoi = roi
                        superBlok = blok
                        update = False

            except:
                print("no black")

        try:
            if superRoi.any() and superBlok.any():
                superRoi = cv2.drawContours(superRoi, [superBlok], 0, (0, 255, 0), 3)

                # centroid
                M = cv2.moments(superBlok)
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                dinko = cv2.circle(superRoi, (cX, cY), 3, (0, 255, 255), -1)
                if (cX > centerX):
                    print("To right")
                else:
                    print("To left")


            cv2.imshow("img", roi)
            cv2.imshow("mask", thresh)
            cv2.imshow("frame", frame)
        except:
            print()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #video.release()
        #cv2.destroyAllWindows()


if __name__ == "__main__":
    main()