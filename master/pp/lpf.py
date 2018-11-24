# Author: Vanessa Fernandez Martinez

from highpassfilter import highpassfilter
import matplotlib.pyplot as plt
import numpy as np
import cv2


def filter(img, frec, n, tpe=""):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Fourier transform
    img_fft = np.fft.fft2(img)
    # Shift the zero-frequency component to the center of the spectrum.
    fft_center = np.fft.fftshift(img_fft)
    # We calculate the Butterworth high pass filter
    HPF = highpassfilter(fft_center.shape, frec, n)
    if tpe == 'low':
        HPF = 1-HPF
    # We apply the filter on the centered Fourier transform
    img_fil = HPF * fft_center
    # We move the fourier transform
    fft_inv = np.fft.ifftshift(img_fil, axes=None)
    # We do the inverse transform of fourier
    img_org = np.fft.ifft2(fft_inv)
    return img_org, fft_center


def showImage(img, img_org):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Image visualization
    plt.figure()
    plt.subplot(1, 2, 1), plt.title('IFFT uint8'), plt.imshow(img_org.real, cmap='gray')
    plt.subplot(1, 2, 2), plt.title('Original'), plt.imshow(img)
    # Normalize
    A = np.double(img_org.real)
    out = np.zeros(A.shape, np.double)
    normal = cv2.normalize(A, out, 1.0, 0.0, cv2.NORM_MINMAX)
    plt.figure()
    plt.subplot(1, 2, 1), plt.title('Normalize'), plt.imshow(normal, cmap='gray')
    plt.subplot(1, 2, 2), plt.title('Original'), plt.imshow(img, cmap='gray')
    plt.show()


if __name__ == "__main__":
    path = input('What image do you want to filter?: ')
    frec = float(input('Cutoff frequency: '))
    n = int(input('n: '))
    # Read image
    img = cv2.imread(path)
    # Filter
    img_org = filter(img, frec, n, 'low')
    cv2.imwrite("a.jpg", img_org.real)
    # Show the images
    showImage(img, img_org)