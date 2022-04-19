import cv2
import pytesseract
import numpy as np
import os
from PIL import Image


def capture():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # img = cv2.threshold(img, 120, 255, cv2.THRESH_TOZERO)[1]
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        # img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, img)
    cap.release()
    cv2.destroyAllWindows()
    print("filename:", filename)
    return filename


def convert(filename):
    print("starting")
    text1 = pytesseract.image_to_boxes(Image.open(filename))
    text2 = pytesseract.image_to_string(Image.open(filename), config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    print("OCR: ", text2)


filename = capture()
convert(filename)
