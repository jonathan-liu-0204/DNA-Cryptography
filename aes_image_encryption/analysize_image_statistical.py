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



def Entropy(img):
    _, counts = unique(img, return_counts=True)
    return scipy_entropy(counts, base=2)



def Correlation(orig_image, encrypt_image, fig1_name, fig2_name, fig3_name, info_out_file):
    f = open(info_out_file, "a")

    matrixX, matrixY = getCorrelation(orig_image, 1, 0)
    matrixX2, matrixY2 = getCorrelation(encrypt_image, 1, 0)
    f.write('\nCorrelation Coefficient: \n')
    corHorizontal = np.corrcoef(matrixX2, matrixY2)
    f.write('Horizontal: ' + str(round(corHorizontal[1, 0],4)) + "\n")

    matplotlib.style.use('ggplot')
    plt.subplot(122), plt.scatter(matrixX2, matrixY2,c='blue', alpha=0.5), plt.title('Horizontal')
    plt.subplot(121), plt.scatter(matrixX, matrixY,c='blue', alpha=0.5), plt.title('ORIGINAL')
    plt.savefig(fig1_name)


    matrixX, matrixY = getCorrelation(orig_image, 0, 1)
    matrixX2, matrixY2 = getCorrelation(encrypt_image, 0, 1)

    corVertical = np.corrcoef(matrixX2, matrixY2)
    f.write('Vertical: ' + str(round(corVertical[1, 0],4)) + "\n")

    matplotlib.style.use('ggplot')
    plt.subplot(122), plt.scatter(matrixX2, matrixY2,c='blue', alpha=0.5), plt.title('Vertical')
    plt.subplot(121), plt.scatter(matrixX, matrixY,c='blue', alpha=0.5), plt.title('ORIGINAL')
    plt.savefig(fig2_name)

    matrixX, matrixY = getCorrelation(orig_image, 1, 1)
    matrixX2, matrixY2 = getCorrelation(encrypt_image, 1, 1)

    corDiagonal = np.corrcoef(matrixX2, matrixY2)
    f.write('Diagonal: ' + str(round(corDiagonal[1,0],4)) + "\n")

    matplotlib.style.use('ggplot')
    plt.subplot(122), plt.scatter(matrixX2, matrixY2,c='blue', alpha=0.5), plt.title('Diagonal')
    plt.subplot(121), plt.scatter(matrixX, matrixY,c='blue', alpha=0.5), plt.title('ORIGINAL')
    plt.savefig(fig3_name, dpi=300)

    f.close()



# x=1 y=0  horizontal    
# x=0 y=1  vertical    
# x=1 y=1  diagonal
def getCorrelation(img, x, y):
    correlationcCount = 8000
    
    matrixX = []
    matrixY = []

    rows, cols = img.shape

    maxRow = rows-1
    maxCol = cols-1
    if x==0 and y==1:
        maxCol=cols
    if x==1 and y==0:
        maxRow=rows

    random.seed(1)
    for i in range(correlationcCount):
        rx = random.randint(0, maxRow-2)
        ry = random.randint(0, maxCol-2)
        matrixX.append(img[rx,ry])
        matrixY.append(img[rx+x,ry+y])

    return matrixX, matrixY



def showImage(orig_image, encrypt_image, fig_name):
    plt.subplot(231), plt.imshow(orig_image, cmap='gray',vmin=0, vmax=255), plt.title('ORIGINAL')
    plt.subplot(232), plt.imshow(encrypt_image, cmap='gray',vmin=0, vmax=255), plt.title('AES')
    hist1 = cv2.calcHist([orig_image], [0], None, [256], [0, 256])
    hist3 = cv2.calcHist([encrypt_image], [0], None, [256], [0, 256])

    plt.subplot(234), plt.hist(orig_image.ravel(), 256, [0, 256])
    plt.subplot(235), plt.hist(encrypt_image.ravel(), 256, [0, 256])

    plt.savefig(fig_name)



