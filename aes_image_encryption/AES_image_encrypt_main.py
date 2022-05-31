# Reference: https://github.com/user163/image-encryption
#            https://github.com/mehdim7/RNA-DNA-Image-Encryption?fbclid=IwAR1fVUzH28JDl-bWAIp5tfUE-og7-FX2GZF7-AkDJReCPcKB7xTD1GtvqKM


import sys
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time
from aes_image import *
from analysize_image_statistical import *
from analysize_image_sensibility import *
from PIL import Image



def main():
    # Set Mode (Only Support AES.MODE_CBC and AES.MODE_ECB)
    mode_name = '_cbc'
    mode = AES.MODE_CBC
    if mode != AES.MODE_CBC and mode != AES.MODE_ECB:
        print('Only CBC and ECB mode supported...')
        sys.exit()

    # Set Key and IV Size
    key = "abcdefghijklmnop"
    # key = None
    key_size = 32
    iv_size = AES.block_size if mode == AES.MODE_CBC else 0

    # Set Target Image Name
    path = "C:/Users/jonat/Desktop/DNA-Cryptography/aes_image_encryption/Dataset/"
    # C:\Users\jonat\Desktop\DNA-Cryptography\aes_image_encryption\Dataset
    img_num = '66'
    img = path + img_num + ".jpg"
    img_enc = path + "img_enc" + img_num + mode_name + ".bmp"
    img_dec = path + "img_dec" + img_num + mode_name + ".bmp"
    img_enc_gray = path + "img_enc_gray" + img_num + mode_name + ".png"
    img_orig_gray = path + "img_orig_gray" + img_num + mode_name + ".png"
    img_cor_horizontal = path + "img_cor_horizontal" + img_num + mode_name + ".png"
    img_cor_vertical = path + "img_cor_vertical" + img_num + mode_name + ".png"
    img_cor_diagonal = path + "img_cor_diagonal" + img_num + mode_name + ".png"
    img_hist = path + "img_hist" + img_num + mode_name + ".png"
    info_out_file = path + "img_info" + img_num + mode_name + ".txt"


    start = time.time()

    # AES_IMAGE Initailization
    aes = AES_IMAGE(mode = mode, key_size = key_size, iv_size = iv_size)
    orig_image = aes.load_image(img_name = img)
    aes.check_min_width()
    # aes.display_orig_img()


    # Encryption
    encrypt_image = aes.encrypt(key = key)
    end = time.time()
    aes.display_encry_img()
    aes.save_encrypt_img(img_enc)

    print("Time for Encryption: " + str(round(end-start,3)))
    f = open(info_out_file, "w")
    f.write("Time for Encryption: " + str(round(end-start,3)) + "\n")
    f.close()


    # Decryption
    decrypt_image = aes.decrypt()
    aes.display_decry_img()
    aes.save_decrypt_img(img_dec)


    # Convert to Grayscale
    orig_image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(img_orig_gray, orig_image)
    encrypt_image = cv2.imread(img_enc, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(img_enc_gray, encrypt_image)


    # Statistical Analysis
    start = time.time()
    
    f = open(info_out_file, "a")
    f.write("\nStatistical Analysis: \n")
    f.close()
    
    Correlation(orig_image, encrypt_image, img_cor_horizontal, img_cor_vertical, img_cor_diagonal, info_out_file)
    showImage(orig_image, encrypt_image, img_hist)

    end = time.time()
    print("Time for Statistical Analysis: " + str(round(end-start,3)))


    # Sensibility Analysis
    start = time.time()

    f = open(info_out_file, "a")
    f.write("\nSensibility Analysis: \n")
    f.write("\nEntropy: \n")
    f.write("Entropy for Original Image: " + str(Entropy(orig_image)) + "\n")
    f.write("Entropy for Encrypted Image: " + str(Entropy(encrypt_image)) + "\n")
    f.close()
    
    NPCRUACI(img, mode, key, key_size, iv_size, info_out_file)

    end = time.time()
    print("Time for Sensibility Analysis: " + str(round(end-start,3)))


    cv2.destroyAllWindows()




if __name__ == '__main__':
    main()

