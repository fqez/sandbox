import numpy as np
import sys
import cv2

def expandMatrix(Sobel, size):
    for j in range(3, size[1]):
        Sobel = np.insert(Sobel, j, 0, axis=1)
    for i in range(3, size[0]):
        Sobel = np.insert(Sobel, i, 0, axis=0)
    cv2.imwrite("ss.jpg", Sobel)
    return Sobel


def sobel(img, Vkernel, Hkernel):

    v = cv2.filter2D(img, -1, -Vkernel)
    h = cv2.filter2D(img, -1, -Hkernel)

    return v, h


def sobelfft(img, Vkernel, Hkernel):

    fftv = np.fft.fft2(expandMatrix(Vkernel, img.shape))
    ffth = np.fft.fft2(expandMatrix(Hkernel, img.shape))
    cv2.imwrite("results/sobel11.jpg", fftv.real)
    cv2.imwrite("results/sobel22.jpg", ffth.real)
    convv = fftv * img
    convh = ffth * img
    v =  np.fft.ifft2(convv).real
    h = np.fft.ifft2(convh).real
    v[v<0]=0
    h[h<0]=0
    return v, h

if __name__ == "__main__":
    path = str(sys.argv[1])
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    Vkernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Hkernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    v,h = sobel(img, Vkernel, Hkernel)

    img_fft = np.fft.fft2(img)
    vfft,hfft = sobelfft(img_fft, Vkernel, Hkernel)

    cv2.imwrite("results/sobel.jpg", v + h)
    cv2.imwrite("results/sobelV.jpg", v)
    cv2.imwrite("results/sobelH.jpg", h)
    cv2.imwrite("results/sobelVFFT.jpg", vfft)
    cv2.imwrite("results/sobelHFFT.jpg", hfft)