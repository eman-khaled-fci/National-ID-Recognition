# import the necessary packages
from imutils.perspective import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image, ImageEnhance
import output as output
from pytesseract import Output
import base64
import datetime

#some filters
# noise removal

def remove_noise(image):
    return cv2.medianBlur(image,5)
#scanning section
def scan(path):
        # load the image and compute the ratio of the old height
        # to the new height, clone it, and resize it
        image = cv2.imread(path)
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height = 500)

        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        #edged = cv2.Canny(gray, 75, 200)
        edged = cv2.Canny(gray, 150, 200)


        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

        # loop over the contours
        for c in cnts:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                # if our approximated contour has four points, then we
                # can assume that we have found our screen
                if len(approx) == 4:
                        screenCnt = approx
                        break


        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

        # show the original and scanned images
        newimg = cv2.resize(warped,(1000,630))
        cv2.imwrite("temp_front.jpg",newimg)
        return newimg


def crop(path):


        #cropping section

        img = cv2.imread("temp_front.jpg")
        im = Image.open('temp_front.jpg')
        #plt.imshow(im)
        # crop image
        im_crop = im.crop((10, 20, 290, 375))
        im_crop.save('NationalImage.jpg', quality=300000)

        #crop name
        im_crop2 = im.crop((400, 150, 1000, 318))
        im_crop2.save('NationalName.jpg', quality=300000)

        #crop id
        crop = im.crop((440, 500, 1000, 560))
        crop.save('NationalIdPart.jpg', quality=10000)


        #extracting text section
        custom_config = r'--oem 3 --psm 6'

        # read id part
        img = cv2.imread('NationalIdPart.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 199, 41)
        NationalIdTextPart1 = pytesseract.image_to_string(img, config=r'--oem 3 --psm 6', lang="ara_number_id")
        IDNumberPart1 = ''.join(NationalIdTextPart1.split())
        #print(IDNumberPart1)

        # read name part
        imge = cv2.imread('NationalName.jpg')
        imge = cv2.cvtColor(imge, cv2.COLOR_BGR2GRAY)
        imge = cv2.adaptiveThreshold(imge, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 199, 42)
        NationalNameTextPart1 = pytesseract.image_to_string(imge, config=custom_config, lang="ara")
        NationalName = NationalNameTextPart1.replace('\r', '').replace('\n', ' ')
        #print(NationalName)


        #read image part
        NationalImage = cv2.imread('NationalImage.jpg')
        #convert image to base64 string
        jpg_img = cv2.imencode('.jpg', NationalImage)
        b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
        #print(b64_string)

        #retun from national id :Name in string form , id in string form , image in base64 string form
        return NationalNameTextPart1,IDNumberPart1,b64_string

def time(self):
        return datetime.datetime.now()

def extractInfo(path):
      return crop(scan(path))