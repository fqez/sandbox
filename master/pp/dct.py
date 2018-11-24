# Author: Vanessa Fernandez Martinez

import numpy as np
import matplotlib.pyplot as plt
import cv2


def dctC(img, size, mask):
    # Do 8x8 DCT on image
    i = 0
    DCT = np.zeros((size[0], size[1]), np.float32)
    while i < size[0]:
        j = 0
        while j < size[1]:
            DCT[i:i+8, j:j+8] = cv2.dct(np.float32(img[i:i+8, j:j+8])) * mask
            j += 8
        i += 8
    return DCT


def idctC(img, size):
    # Do 8x8 IDCT on image
    i = 0
    IDCT = np.zeros((size[0], size[1]), np.float32)
    while i < size[0]:
        j = 0
        while j < size[1]:
            IDCT[i:i+8, j:j+8] = cv2.idct(np.float32(img[i:i+8, j:j+8]))
            j += 8
        i += 8
    IDCT = np.uint8(IDCT)
    return IDCT


def processCompress(img, size, mask):
    # DCT
    DCT = dctC(img, size, mask)
    # IDCT
    IDCT = idctC(DCT, size)
    plt.figure()
    plt.subplot(1, 2, 1), plt.title('DCT'), plt.imshow(DCT, cmap='gray')
    plt.subplot(1, 2, 2), plt.title('IDCT'), plt.imshow(IDCT, cmap='gray')

def cc(n):

    b = np.array([1, 3, 6, 10, 15, 21, 28, 36])
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8])

    return int(a[np.where(b == n)[0]])

def create_mask(ratio):
    a = np.triu(np.ones(ratio))  # this is for quantising w/ mask
    W = np.zeros((8, 8))
    W[:ratio, 8-ratio:] = a
    W = np.fliplr(W)
    return W


if __name__ == "__main__":
    path = input('What image do you want to do a DCT?: ')
    # Read image
    img = cv2.imread(path)
    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Size of image
    size = img.shape

    # Without compression
    # Mask
    mask1 = np.array([[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]])

    processCompress(img, size, mask1)

    # Compression factor 1/64
    mask_1_64 = np.array([[1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])

    processCompress(img, size, mask_1_64)

    # Compression factor 10/64
    mask_10_64 = np.array(
        [[1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])

    processCompress(img, size, mask_10_64)

    # Compression factor 21/64
    mask_21_64 = np.array(
        [[1, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0],
         [1, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])

    processCompress(img, size, mask_21_64)
    plt.show()