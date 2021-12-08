from lib import *

def findZeroCrossings(img):
    """takes in an input np.array and returns and 'image-able' array with 255's where there were zero crossings and 0's
        everywhere else.
    """

    hozDiff = np.gradient(img, axis=0)
    vertDiff = np.gradient(img, axis=1)

    hozthres = np.percentile(hozDiff, 96)
    vertThres = np.percentile(vertDiff, 96)

    hozEdgeImg = (hozDiff > hozthres) * np.uint8(255)
    vertEdgeImg = (vertDiff > vertThres) * np.uint8(255)

    edgeimg = np.uint8(((hozEdgeImg+vertEdgeImg)/510)*255)

    edgeimg = (edgeimg > 100) * np.uint8(255)

    return edgeimg
