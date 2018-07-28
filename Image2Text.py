import pytesseract
import cv2
import os


def image2text(path, blur=False):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if blur == True:
        gray = cv2.medianBlur(gray, 3)
    text = pytesseract.image_to_string(gray)
    return text
