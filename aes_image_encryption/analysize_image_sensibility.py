# Reference: https://github.com/user163/image-encryption
#            https://github.com/mehdim7/RNA-DNA-Image-Encryption?fbclid=IwAR1fVUzH28JDl-bWAIp5tfUE-og7-FX2GZF7-AkDJReCPcKB7xTD1GtvqKM



import random
import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from numpy import unique
from scipy.stats import entropy as scipy_entropy
import time
from aes_image import *
import os



def getNextPixcel(pixcel):
    if (pixcel == 255):
        pixcel = 0
    else:
        pixcel += 1
    return pixcel



def NPCRUACI(img_name, mode, key, key_size, iv_size, info_out_file):
    f = open(info_out_file, "a")
    f.write("\nNPCRUACI: \n")

    # Run 1
    img1 = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    img1[0, 0] = getNextPixcel(img1[0, 0])
    rows, cols = img1.shape
    cv2.imwrite("t1.png", img1)

    aes1 = AES_IMAGE(mode = mode, key_size = key_size, iv_size = iv_size)
    aes1.load_image(img_name = "t1.png")
    aes1.check_min_width()
    encrypt_image_run1 = aes1.encrypt(key = key)
    cv2.imwrite("t2.png", encrypt_image_run1)

    orig_image_run1 = cv2.imread("t1.png", cv2.IMREAD_GRAYSCALE)
    encrypt_image_run1 = cv2.imread("t2.png", cv2.IMREAD_GRAYSCALE)
    NPCR1, UACI1 = getEachNPCRUACI(orig_image_run1, encrypt_image_run1)
    f.write('First Pixcel: \n')
    f.write('NPCR: ' + str(round(NPCR1,6)) + "\n")
    f.write('UACI: ' + str(round(UACI1,6)) + "\n")

    
    # Run 2
    img2 = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    img2[int(rows / 2), int(cols / 2)] = getNextPixcel(img2[int(rows / 2), int(cols / 2)])
    cv2.imwrite("t1.png", img2)

    aes2 = AES_IMAGE(mode = mode, key_size = key_size, iv_size = iv_size)
    aes2.load_image(img_name = "t1.png")
    aes2.check_min_width()
    encrypt_image_run2 = aes2.encrypt(key = key)
    cv2.imwrite("t2.png", encrypt_image_run2)

    orig_image_run2 = cv2.imread("t1.png", cv2.IMREAD_GRAYSCALE)
    encrypt_image_run2 = cv2.imread("t2.png", cv2.IMREAD_GRAYSCALE)
    NPCR2, UACI2 = getEachNPCRUACI(orig_image_run2, encrypt_image_run2)
    f.write('Midle Pixcel: \n')
    f.write('NPCR: ' + str(round(NPCR1,6)) + "\n")
    f.write('UACI: ' + str(round(UACI1,6)) + "\n")


    # Run 3
    img3 = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    img3[rows - 1, cols - 1] = getNextPixcel(img3[rows - 1, cols - 1])
    cv2.imwrite("t1.png", img3)

    aes3 = AES_IMAGE(mode = mode, key_size = key_size, iv_size = iv_size)
    aes3.load_image(img_name = "t1.png")
    aes3.check_min_width()
    encrypt_image_run3 = aes3.encrypt(key = key)
    cv2.imwrite("t2.png", encrypt_image_run3)

    orig_image_run3 = cv2.imread("t1.png", cv2.IMREAD_GRAYSCALE)
    encrypt_image_run3 = cv2.imread("t2.png", cv2.IMREAD_GRAYSCALE)
    NPCR3, UACI3 = getEachNPCRUACI(orig_image_run3, encrypt_image_run3)
    f.write('Last Pixcel: \n')
    f.write('NPCR: ' + str(round(NPCR1,6)) + "\n")
    f.write('UACI: ' + str(round(UACI1,6)) + "\n")


    # Average
    NPCR4 = (NPCR1 + NPCR2 + NPCR3) / 3
    UACI4 = (UACI1 + UACI2 + UACI3) / 3
    f.write('Average: \n')
    f.write('NPCR: ' + str(round(NPCR4,6)) + "\n")
    f.write('UACI: ' + str(round(UACI4,6)) + "\n")

    os.remove("t1.png")
    os.remove("t2.png")
    f.close()
    


def getEachNPCRUACI(img1, img2):

    rows, cols = img1.shape
    sumNPCR = 0
    sumUACI = 0
    for i in range(rows):
        for j in range(cols):
            sumUACI += abs(int(img1[i, j]) - int(img2[i, j]))
            if (img1[i, j] != img2[i, j]):
                sumNPCR += 1
    NPCR = sumNPCR / (rows * cols)
    UACI = sumUACI / (255 * rows * cols)

    return NPCR, UACI