import numpy as np
import matplotlib.pyplot as plt
import cv2

def dctC(img, size, mask):
    # Do 8x8 DCT on image
    i = 0
    DCT = np.zeros((size[0], size[1]), np.float32)
    while i < size[0]-1:
        j = 0
        while j < size[1]-1:
            a = img[i:i+8, j:j+8]
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


def dct_idct(img, size, mask):
    # DCT
    DCT = dctC(img, size, mask)
    # IDCT
    IDCT = idctC(DCT, size)
    return DCT, IDCT


def create_mask(n):

    # obtain the size of the upper triangular matrix
    b = np.array([1, 3, 6, 10, 15, 21, 28, 36])
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    ratio = int(a[np.where(b == n)[0]])

    # generate 8x8 mask
    a = np.triu(np.ones(ratio))  # this is for quantising w/ mask
    W = np.zeros((8, 8))
    W[:ratio, 8-ratio:] = a
    W = np.fliplr(W)
    return W

def dct_main(img):
    size = img.shape
    c = np.array([1, 3, 6, 10, 15, 21, 28, 36])
    compressions = np.empty((8,), dtype=object)
    compressions[:] = [np.zeros([8, 8], dtype=int) * len(compressions)]
    for i in range(np.size(c)):
        compressions[i] = create_mask(c[i])

    print(compressions)

    for i in range(np.size(c)):
        dct, idct = dct_idct(img, size, compressions[i])
        namedct = "results/comp_" + str(c[i]) + "_dct.jpg"
        nameidct = "results/comp_" + str(c[i]) + "_idct.jpg"
        cv2.imwrite(namedct, dct)
        cv2.imwrite(nameidct, idct)

if __name__ == "__main__":
    path = input('What image do you want to do a DCT?: ')
    # Read image
    img = cv2.imread(path)
    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Size of image
    dct_main(img)

