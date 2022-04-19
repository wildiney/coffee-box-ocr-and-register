"""
OCR WITH PYTESSERACT
Read the image files on images folder and
writes the text on the codes.txt file
"""

import os
import shutil

import cv2
import numpy as np
import pytesseract as ocr

from PIL import Image


def main():
    print("Starting Script")
    files = listFiles()
    for file in files:
        print(convert(file))


def convert(file, debug=False):
    try:
        imagem = Image.open(file).convert('RGB')

        npimagem = np.asarray(imagem).astype(np.uint8)

        npimagem[:, :, 0] = 0
        npimagem[:, :, 2] = 0

        im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY)

        ret, thresh = cv2.threshold(
            im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        binimagem = Image.fromarray(thresh)
        if debug is True:
            binimagem.show()

        phrase = ocr.image_to_string(binimagem, lang="por")
        if len(phrase) > 0:
            shutil.move(file, file+".bak")
            f = open("codes.txt", "a+")
            f.write(phrase+"\r")
            f.close()
            return phrase
        else:
            return "File " + file + " is unreadable"
    except FileNotFoundError:
        return "File " + file + " not found"


def listFiles(dir="images"):
    namefiles = []
    files = os.listdir(dir)
    for file in files:
        if file.endswith(".jpg"):
            namefiles.append("images/"+file)

    return namefiles


if __name__ == "__main__":
    main()
