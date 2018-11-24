import numpy as np

def cc(n):

    b = np.array([1, 3, 6, 10, 15, 21, 28, 36])
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    c = int(a[np.where(b == n)[0]])
    print (c)
    return c

def create_mask(ratio):
    a = np.triu(np.ones(ratio))  # this is for quantising w/ mask
    W = np.zeros((8, 8))
    W[:ratio, 8-ratio:] = a
    W = np.fliplr(W)
    return W


x = create_mask(cc(10))
print (x)

