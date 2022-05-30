# Reference: https://github.com/user163/image-encryption
#            https://github.com/mehdim7/RNA-DNA-Image-Encryption?fbclid=IwAR1fVUzH28JDl-bWAIp5tfUE-og7-FX2GZF7-AkDJReCPcKB7xTD1GtvqKM



import sys
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time



class AES_IMAGE:
    def __init__(self, mode, key_size, iv_size):
        self.mode = mode
        self.key_size = key_size
        self.iv_size = iv_size


    def load_image(self, img_name):
        self.image_orig = cv2.imread(img_name)
        self.row_orig, self.column_orig, self.depth_orig = self.image_orig.shape

        return self.image_orig


    def check_min_width(self):
        self.min_width = (AES.block_size + AES.block_size)
        if self.column_orig < self.min_width:
            print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(self.min_width))
            sys.exit()


    def display_orig_img(self):
        cv2.imshow("Original Image", self.image_orig)
        cv2.waitKey()


    def img_to_byte(self, img):
        image_bytes = img.tobytes()
        return image_bytes


    def encrypt(self, key):
        image_orig_bytes = self.img_to_byte(self.image_orig)

        if key == None:
            self.key = get_random_bytes(self.key_size)
        else:
            key_bytes = bytes(key, 'UTF-8')
            self.key = key_bytes

        iv = get_random_bytes(self.iv_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv) if self.mode == AES.MODE_CBC else AES.new(self.key, AES.MODE_ECB)
        image_orig_bytes_padded = pad(image_orig_bytes, AES.block_size)
        ciphertext = cipher.encrypt(image_orig_bytes_padded)

        # Convert Ciphertext Bytes to Encrypted Image Data
        padded_size = len(image_orig_bytes_padded) - len(image_orig_bytes)
        void = self.column_orig * self.depth_orig - self.iv_size - padded_size
        iv_ciphertext_void = iv + ciphertext + bytes(void)
        self.image_encrypted = np.frombuffer(iv_ciphertext_void, dtype = self.image_orig.dtype).reshape(self.row_orig + 1, self.column_orig, self.depth_orig)

        return self.image_encrypted


    def display_encry_img(self):
        cv2.imshow("Encrypted Image", self.image_encrypted)
        cv2.waitKey()


    def save_encrypt_img(self, img_name):
        cv2.imwrite(img_name, self.image_encrypted)
        

    def decrypt(self):
        # Convert Encrypted Image Data to Ciphertext Bytes
        self.row_encrypted, self.column_orig, self.depth_orig = self.image_encrypted.shape 
        self.row_orig = self.row_encrypted - 1
        encrypted_bytes = self.img_to_byte(self.image_encrypted)
        iv = encrypted_bytes[:self.iv_size]
        image_orig_bytes_size = self.row_orig * self.column_orig * self.depth_orig
        padded_size = (image_orig_bytes_size // AES.block_size + 1) * AES.block_size - image_orig_bytes_size
        encrypted = encrypted_bytes[self.iv_size : self.iv_size + image_orig_bytes_size + padded_size]

        cipher = AES.new(self.key, AES.MODE_CBC, iv) if self.mode == AES.MODE_CBC else AES.new(self.key, AES.MODE_ECB)
        decrypted_image_bytes_padded = cipher.decrypt(encrypted)
        decrypted_image_bytes = unpad(decrypted_image_bytes_padded, AES.block_size)

        # Convert Bytes to Decrypted Image Data
        self.decrypted_image = np.frombuffer(decrypted_image_bytes, self.image_encrypted.dtype).reshape(self.row_orig, self.column_orig, self.depth_orig)

        return self.decrypted_image


    def display_decry_img(self):
        cv2.imshow("Decrypted Image", self.decrypted_image)
        cv2.waitKey()


    def save_decrypt_img(self, img_name):
        cv2.imwrite(img_name, self.decrypted_image)