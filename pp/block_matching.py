import numpy as np
import cv2
from threading import Thread
import threading
import multiprocessing
import math

KERNEL_SIZE = 11
HALF_KERNEL = int(math.floor(KERNEL_SIZE / 2))
MAX_DISPARITY = 50
N_THREADS = 4

debug = [0,1,3,5]
#debug = [-1, -3, -5]
#debug = [-10]

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def loadImage(path):
    img = cv2.imread(path)
    return img

# Recibe 2 bloques de 11x11 y es aplica sad
def sad(b1, b2):
    return 1 / (1 + np.sum(np.sum(np.abs(b2 - b1))))

def ssd(b1, b2):
    x = b2 - b1
    return 1 / (1 + (np.sum(np.sum(x**2))))

def get_block(img, x, y):
    return img[x-HALF_KERNEL:x+HALF_KERNEL+1, y-HALF_KERNEL:y+HALF_KERNEL+1]

def match(im1, im2, depth, index_rows, tn, ret):

    size = depth.shape

    for rows in range(index_rows[0], index_rows[1]):
        #print("thread:", tn, rows)
        for cols in range(HALF_KERNEL, size[1]-HALF_KERNEL):

            #b1 = im1[rows-HALF_KERNEL:rows+HALF_KERNEL, cols-HALF_KERNEL:cols+HALF_KERNEL]
            b1 = get_block(im1, rows, cols)
            best = 0
            ant = -999999
            for o in range(MAX_DISPARITY):

                #b2 = im2[rows-HALF_KERNEL:rows+HALF_KERNEL, (cols+o)-HALF_KERNEL:(cols+o)+HALF_KERNEL]
                b2 = get_block(im2, rows, cols+o)
                if cols+o+HALF_KERNEL > size[1]-1:
                    break
                ssd_val = ssd(b1, b2)
                if ssd_val > ant:
                    ant = ssd_val
                    best = o

            depth[rows-index_rows[0], cols] = best * (255/MAX_DISPARITY)
            cv2.imshow("d"+str(tn), depth)
            cv2.waitKey(1)

    ret[tn] = depth

if __name__ == "__main__":

    pathR = 'images/tl1.jpg'
    pathL = 'images/tl2.jpg'

    imR = loadImage(pathR)
    imL = loadImage(pathL)
    #imL=cv2.resize(imL,(320,240))
    #imR=cv2.resize(imR, (320, 240))

    imR = cv2.cvtColor(imR, cv2.COLOR_RGB2GRAY)
    imL = cv2.cvtColor(imL, cv2.COLOR_RGB2GRAY)

    depth = np.zeros((imL.shape[0], imL.shape[1]), np.uint8)
    chunk = int(depth.shape[0] / N_THREADS)

    if 0 in debug:
        print(imL.shape)
        print(imR.shape)
        print(depth.shape)
        print(chunk)

    threads = [None] * N_THREADS
    results = [None] * N_THREADS

    # ------------- single thread ----------------
    #d = match(imR, imL, depth, (0,imL.shape[1]), -1)
    #cv2.imwrite("images/result.jpg", d)
    #cv2.imshow("d", d)
    #cv2.waitKey(0)
    # --------- end single thread ---------------

    # --------------- multithread -------------
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(len(threads)):
        p = multiprocessing.Process(target=match, args=(imL, imR, depth[i*chunk:i*chunk+chunk,:].copy(),(i*chunk,i*chunk+chunk),i,return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    import operator

    chunked_images = sorted(return_dict.items(), key=operator.itemgetter(0))

    imLR = np.zeros((0,imL.shape[1]),np.uint8)
    for i in range(N_THREADS):
        im = chunked_images[i][1]
        cv2.imshow("Thread "+str(i), im)
        imLR = np.concatenate((imLR, im), axis=0)

    cv2.imshow("Result", imLR)
    cv2.waitKey(0)

    #------------ end multithread ----------------

    cv2.destroyAllWindows()
