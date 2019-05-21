import cv2
import math


def main():
    cap = cv2.VideoCapture(0)
    test = True

    while True:
        # test = False
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            try:
                c = getSmallest(contours)
                print(c)
                frame = cv2.drawContours(frame, [c], 0, (0, 255, 0), 3)

                # centroid
                M = cv2.moments(c)
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                center = cv2.circle(frame, (cX, cY), 3, (0, 255, 255), -1)
            except:
                print("no black")

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(0)


def getSmallest(contours):
    d = 1
    e = None

    for i in range(len(contours)):
        c = contours[i]
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
        area = cv2.contourArea(c)
        if area < 500:
            continue
        perimeter = cv2.arcLength(c, True)
        factor = 1

        if perimeter > 0:
            factor = 4 * math.pi * area / perimeter**2

        if 2 < len(approx) < 6:
            if factor < d:
                d = factor
                e = c
    print(4 * math.pi * cv2.contourArea(e) / cv2.arcLength(e, True)**2)
    return e


if __name__ == "__main__":
    main()