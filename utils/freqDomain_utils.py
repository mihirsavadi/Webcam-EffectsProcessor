from lib import *

def GaussianFilterFreqDomain(frame: np.array, sigma: float) -> np.array :
    """Performs gaussian filtering in the frequency domain on a grayscale input image, 
        or alternatively just one channel

    Parameters
    ----------
    img : np.array
        input fram
    filter : np.array
        gaussian transfer function. presized because input frame size is known.
    param : int, optional
        sigma for , by default 10

    Returns
    -------
    np.array
        [description]
    """

    # get size of frame and pad accordingly
    rows, cols = frame.shape
    img_padded = cv2.copyMakeBorder(frame, 0, rows, 0, cols, cv2.BORDER_REFLECT)

    # multiply padded frame by (-1)^(x+y) to center in the fourier transform
    rows_padded, cols_padded = img_padded.shape
    rowgrid_padded, colgrid_padded = np.mgrid[0:rows_padded:1, 0:cols_padded:1]
    centeringCoeff = (np.power(-1, rowgrid_padded+colgrid_padded))

    img_padded_centered = img_padded * centeringCoeff

    # get dft of padded centered image
    img_fourier = np.fft.fft2(img_padded_centered)

    # get transfer function
    rows_padded_centered, cols_padded_centered = img_padded_centered.shape
    center_padded_centered = (np.uint(np.round(rows_padded_centered/2)), np.uint(np.round(cols_padded_centered/2)))
    rowgrid_padded_centered, colgrid_padded_centered = np.mgrid[0:rows_padded_centered:1, 0:cols_padded_centered:1]

    rowgrid_padded_centered = np.abs(rowgrid_padded_centered - center_padded_centered[0])
    colgrid_padded_centered = np.abs(colgrid_padded_centered - center_padded_centered[1])

    distance = np.sqrt(np.power(rowgrid_padded_centered, 2) + np.power(colgrid_padded_centered, 2))

    transferFunction = np.exp(-(np.power(distance, 2))/(2*np.power(sigma, 2)))
    
    # do forier multiply with transfer function and get filtered image
    img_filtered_padded_centered = np.real(np.fft.ifft2(img_fourier*transferFunction))

    # multiply image by (-1)^(x+y) to un-center it again
    img_filtered_padded = img_filtered_padded_centered * centeringCoeff

    # unpad to get final image
    img_filtered_cropped = img_filtered_padded[0:rows, 0:cols]
    img_filtered = (img_filtered_cropped/np.amax(img_filtered_cropped))


    return img_filtered