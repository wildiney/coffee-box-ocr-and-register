from classes.py_ocr_api import OCR
from config.config import config

while True:
    ocr = OCR(config["apikey"], config["file"])
    new_file = ocr.capture()
    try:
        resultapi = ocr.convert_using_api(new_file)
        if resultapi is not None:
            print(resultapi)
    except Exception as e:
        print(e)
        answer = input(
            "API Server offline. Would you like to try the offline mode? (Y/n)"
            )
        if answer == "y":
            ocr.convert(new_file)
        else:
            break

    newcode = input("Would like to insert a new code? (y/n): ")

    if newcode == "n":
        print("Bye!")
        break
    elif newcode == "y":
        print("Let's insert a new code!")
        pass
    else:
        print("Option not available. Bye!")
        break
