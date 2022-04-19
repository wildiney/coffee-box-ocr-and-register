import cv2
import pytesseract
import os
import requests
import json
from datetime import date
from PIL import Image
from config.config import config


class OCR:
    def __init__(self, apikey, file):
        self.apikey = apikey
        self.file = file

    @staticmethod
    def write_file(content, output, mode="a"):
        print("Writing File...")
        with open(output, mode) as f:
            f.writelines(content)

    @staticmethod
    def capture():
        print("Capturing...")
        filename = "{}-{}.jpg".format(date.today(), os.getpid())
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, None, fx=0.5, fy=0.5,
                             interpolation=cv2.INTER_AREA)
            cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('\r'):
                cv2.imwrite(
                    config["dir_to_save_img"] + filename,
                    img
                    )

                cap.release()
                cv2.destroyAllWindows()
                break

        print("Saving file as", filename)
        return config["dir_to_save_img"]+filename

    def convert(self, filename):
        print("Converting...")
        code = pytesseract.image_to_string(
            Image.open(filename),
            config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
            "0123456789 --psm 6'
        )
        print(code)
        verify = input("It is correct? (y/n): ")
        if verify == "y":
            with open(self.file, 'a') as f:
                f.writelines(f"{code}\n")
        elif verify == "n":
            print("Trying again")
            self.convert(self.capture())

    def convert_using_api(self, filename):
        api_key = self.apikey
        url_api = "https://api.ocr.space/parse/image"

        with open(filename, 'rb') as f:
            get_result = requests.post(
                url_api, files={"filename": f}, data={"apikey": api_key})

        get_result_decoded = get_result.content.decode()
        result = json.loads(get_result_decoded).get(
            "ParsedResults")[0].get("ParsedText")
        print(result)
        verify = input("It is correct? (y/n): ")
        if verify == "y":
            self.write_file(result, self.file)
        elif verify == "n":
            print("Let's try again")
            self.convert_using_api(self.capture())
        else:
            print("Option not available. Exiting now.")
