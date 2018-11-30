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

    print("thread",tn)
    #print(HALF_KERNEL)
    size = depth.shape
    ssd_val = 0

    for rows in range(index_rows[0], index_rows[1]):
        #print("thread:", tn, rows)
        for cols in range(HALF_KERNEL, size[1]-HALF_KERNEL):
            #print("thread:", tn, rows,cols)

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
                #print(ssd_val)
                if ssd_val > ant:
                    ant = ssd_val
                    best = o
                    #print(best)

            depth[rows-index_rows[0], cols] = best * (255/MAX_DISPARITY)
            cv2.imshow("d"+str(tn), depth)
            cv2.waitKey(1)

            #cv2.imshow("d", depth)
            #cv2.waitKey(0)

    ret[tn] = depth


if __name__ == "__main__":

    pathR = 'images/tl1.jpg'
    pathL = 'images/tl2.jpg'

    imR = loadImage(pathR)
    imL = loadImage(pathL)
    imL=cv2.resize(imL,(320,240))
    imR=cv2.resize(imR, (320, 240))

    imR = cv2.cvtColor(imR, cv2.COLOR_RGB2GRAY)
    imL = cv2.cvtColor(imL, cv2.COLOR_RGB2GRAY)

    depth = np.zeros((imL.shape[0], imL.shape[1]), np.uint8)
    chunk = int(depth.shape[0] / N_THREADS)

    if 0 in debug:
        print(imL.shape)
        print(imR.shape)
        print(depth.shape)
        print(chunk)


    lock = threading.Lock()
    threads = [None] * N_THREADS
    results = [None] * N_THREADS

    #d = match(imR, imL, depth, (0,imL.shape[1]), -1)
    #cv2.imwrite("images/result.jpg", d)
    #cv2.imshow("d", d)
    #cv2.waitKey(0)


    '''
    for i in range(len(threads)):
        threads[i] = ThreadWithReturnValue(target=match, args=(imL, imR, depth[i*chunk:i*chunk+chunk,:].copy(),(i*chunk,i*chunk+chunk),i))
        threads[i].start()

    # do some other stuff

    imLR = np.zeros((chunk,320))
    for i in range(len(threads)):
        results[i] = threads[i].join()
        name = "d" + str(i)
        cv2.imwrite("images/results/"+name+".jpg", results[i])
        #cv2.imshow(name, results[i])
        imLR = np.concatenate((imLR, results[i]), axis=0)

    #name = "d" + str(i)
    cv2.imshow("r", imLR)
    '''
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

    imLR = np.zeros((0,320),np.uint8)
    for i in range(N_THREADS):
        im = chunked_images[i][1]
        cv2.imshow("aa"+str(i), im)
        imLR = np.concatenate((imLR, im), axis=0)

    cv2.imshow("A", imLR)
    cv2.waitKey(0)



    # do some other stuff
    '''
    imLR = np.zeros((chunk,320))
    for i in range(len(threads)):
        results[i] = threads[i].join()
        print(results[i])
        name = "d" + str(i)
        cv2.imwrite("images/results/"+name+".jpg", results[i])
        #cv2.imshow(name, results[i])
        imLR = np.concatenate((imLR, results[i]), axis=0)

    #name = "d" + str(i)
    cv2.imshow("r", imLR)
    '''


    #depth = match(imL, imR, depth)
    #cv2.imshow("im1", imL)
    #cv2.imshow("im2", imR)
    #cv2.imshow("depth", depth)

    #imL1 = imL[:100, :]
    #imL2 = imL[100:, :]
    #imLR = np.concatenate((imL1, imL2), axis=0)
    #cv2.imshow("iml1", imL1)
    #cv2.imshow("iml2", imL2)
    #cv2.imshow("imlr", imLR)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
