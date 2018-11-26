import numpy as np
import cv2
import sys

def highpassfilter(size, frec, n):

    x, y = np.ogrid[:size[0], :size[1]]
    cen_x, cen_y = size[0] / 2, size[1] / 2

    dis = np.sqrt((x - cen_x) ** 2 + (y - cen_y) ** 2)
    LPF = 1 / (1 + (dis / frec) ** (2 * n))
    HPF = 1 - LPF

    return HPF

def filter(img, frec, n, tpe=""):

    source = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    fft = np.fft.fftshift(np.fft.fft2(source))
    HPF = highpassfilter(fft.shape, frec, n)
    if tpe == 'low':
        HPF = 1-HPF
    filtered = HPF * fft
    result = np.fft.ifft2(np.fft.ifftshift(filtered, axes=None))

    return result, fft

if __name__ == "__main__":

    path = str(sys.argv[1])
    frec = int(sys.argv[2])
    n = int(sys.argv[3])

    img = cv2.imread(path)
    result, _ = filter(img, frec, n, 'low')
    cv2.imwrite("results/lpf.jpg", result.real)
