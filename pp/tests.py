import numpy as np

def cc(n):

    b = np.array([1, 3, 6, 10, 15, 21, 28, 36])
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    c = int(a[np.where(b == n)[0]])
    print (c)
    return c

def create_mask0(ratio):
    a = np.triu(np.ones(ratio))  # this is for quantising w/ mask
    W = np.zeros((8, 8))
    W[:ratio, 8-ratio:] = a
    W = np.fliplr(W)
    return W

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


c = np.array([1, 3, 6, 10, 15, 21, 28, 36])
compressions = np.empty((8,), dtype=object)
compressions[:] = [np.zeros([8, 8], dtype=int) * len(compressions)]
for i in range(np.size(c)):
    compressions[i] = create_mask(c[i])
print(compressions)