# Performance and Security Analysis of AES Image Encryption

---
## How to Run

1. Prepare the image to be encrypted.
2. Move the image to the "*Dataset*" folder.
3. Change the "*img_num*" variable in "*AES_image_encrypt_main.py*" to the name of the image to be encrypted.
4. Set the "*path*" variable in "*AES_image_encrypt_main.py*" to the path of the "*Dataset*" folder. (Can use unix command "$pwd" to find the current working directory)
5. Set "*mode*" variable (ECB or CBC) in "*AES_image_encrypt_main.py*"
6. Set the "*key*" variable in "*AES_image_encrypt_main.py*" (32 bytes, if it is None, the algorithm will generate the key randomly)
7. $ python3 AES_image_encrypt_main.py