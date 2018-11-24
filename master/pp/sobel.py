# Author: Vanessa Fernandez Martinez

import numpy as np
import matplotlib.pyplot as plt
import cv2


def expandMatrix(Sobel, size):
    for j in range(3, size[1]):
        Sobel = np.insert(Sobel, j, 0, axis=1)
    for i in range(3, size[0]):
        Sobel = np.insert(Sobel, i, 0, axis=0)
    return Sobel


def filterSobelOrig(img, SobelH, SobelV):
    # Convolution
    BorderH = cv2.filter2D(img, -1, -SobelH)
    BorderV = cv2.filter2D(img, -1, -SobelV)
    # Show images
    plt.figure()
    plt.subplot(1,2,1),plt.title('Horizontal Border (Image domain)'),plt.imshow(BorderH,cmap = 'gray')
    plt.subplot(1,2,2),plt.title('Vertical Border (Image Domain)'),plt.imshow(BorderV,cmap = 'gray')


def filterSobelFft(img, SobelH, SobelV):
    # Fill the kernel with zeros
    SobelH = expandMatrix(SobelH, img.shape)
    SobelV = expandMatrix(SobelV, img.shape)
    # Fourier Transform
    SobelHFft = np.fft.fft2(SobelH)
    SobelVFft = np.fft.fft2(SobelV)
    # Multiplication in the frequency domain is equivalent to the convolution in the domin of space
    BorderH = SobelHFft * img
    BorderV = SobelVFft * img
    # We do the inverse transform of fourier
    BorderH =  np.fft.ifft2(BorderH).real
    BorderV = np.fft.ifft2(BorderV).real
    # Threshold
    BorderH[BorderH<0]=0
    BorderV[BorderV<0]=0
    # Show images
    plt.figure()
    plt.subplot(1,2,1),plt.title('Horizontal Border (FFT)'),plt.imshow(np.uint8(BorderH),cmap = 'gray')
    plt.subplot(1,2,2),plt.title('Vertical Border (FFT)'),plt.imshow(np.uint8(BorderV),cmap = 'gray')
    plt.show()


if __name__ == "__main__":
    path = input('What image do you want to filter?: ')
    # Read image
    img = cv2.imread(path)
    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Sobel mask
    SobelH = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    SobelV = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    # Sobel filter
    filterSobelOrig(img, SobelH, SobelV)

    # Fourier Transform
    img_fft = np.fft.fft2(img)
    filterSobelFft(img_fft, SobelH, SobelV)