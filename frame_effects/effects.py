from lib import *
import utils.freqDomain_utils
import utils.spatialDomain_utils


class frameEffect():

    def __init__(self):
        self.effectsDict = {
            'cartoonify' : self.cartoonify, 
            'normal'     : self.normalMode,
            'off'        : self.offMode
        }

    def runEffect(self, effect: str, img, param) :

        if effect in self.effectsDict:
            return self.effectsDict[effect](img, param)
        else:
            raise NameError("effect chosen does not exist")

    def normalMode(self, img: np.array, param: int) -> np.array :
        """returns the input

        Parameters
        ----------
        img : np.array
            input image
        param : int
            ignored

        Returns
        -------
        np.array
            just the input image
        """
        return img

    def offMode(self, img: np.array, param: int) -> np.array :
        """Returns a black image of same size as input image

        Parameters
        ----------
        img : np.array
            input image
        param : int
            ignored

        Returns
        -------
        np.array
            black image
        """
        return np.zeros((img.shape[0], img.shape[1], 3))

    def cartoonify(self, img: np.array, param: int) -> np.array:
        """ Cartoonifies an input image.

        Parameters
        ----------
        img : np.array
            Must be an np.array object representing a 3 channel image.

        param : int
            value from 0 to 100 to adjust intensity of cartoonification. 100 being
            the most intense.

        Returns
        -------
        np.array 
            cartoonified image
            
        """

        img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Smooth both grayscale and main image in frequency domain
        img_smoothed_bw = utils.freqDomain_utils.GaussianFilterFreqDomain(img_bw, param*3+50)

        # get edges from img_smoothed_bw
        img_edgeDetect = utils.spatialDomain_utils.findZeroCrossings(img_smoothed_bw)
        # img_edgeDetect = utils.spatialDomain_utils.findZeroCrossings(img_edgeDetect) # uncomment to make thinner
        img_edgeDetect = np.uint8(255 - img_edgeDetect)

        # multiply mask original image
        img_ANDER = (img_edgeDetect == 255) * 1
        img_ANDER = np.repeat(img_ANDER[:, :, np.newaxis], 3, axis=2) # repeat in 3 dimensions

        img_cartoonified = np.multiply(img_ANDER, img)

        img_cartoonified = np.uint8((img_cartoonified/np.amax(img_cartoonified)) * 225)

        return img_cartoonified