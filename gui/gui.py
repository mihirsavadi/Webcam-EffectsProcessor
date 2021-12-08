from lib import *
import frame_effects.effects

class guiClass():

    def __init__(self, windowName):
        """Initialize class before event loop. 
           Also do webcam setup and effects setup here"""

        # initialize effects class
        self.mode = "cartoonify"

        self.effectRunner = frame_effects.effects.frameEffect()

        # initialize webcam and check if opened correctly
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

        # gui setup
        self.windowName = windowName

        cv2.namedWindow(self.windowName)

        # create buttons and sliders
        # # to enable buttons must compile openCV with QT. Pain to do right now.
        # cv2.createButton('Turn OFF', self.button_do, 'off')
        # cv2.createButton('Normal', self.button_do, 'normal')
        # cv2.createButton('Cartoonizer', self.button_do, 'cartoonify')
        # cv2.createButton('Take Picture', self.button_do, 'cartoonify')
        sliders = [
            self.make_slider(1, 100, 0, 'intensity', self.windowName)
        ]

    def eventLoop(self):
        """Event loop for this gui class to be called in an infinite loop
        """

        # get slider values
        param = self.get_slider('intensity', win_name=self.windowName)

        # get webcam frame and get 'effectized' frame
        ret, frame = self.cap.read()
        returned_frame = self.effectRunner.runEffect(self.mode, frame, param)

        # show returned frame
        cv2.imshow(self.windowName, returned_frame)

    def button_do(self, mode: str) :
        """Gets triggered when a button is hit, changing class mode.

        Parameters
        ----------
        mode : str
            the mode corresponding to the button hit
        """
        if mode == 'Take Picture':
            param = self.get_slider('intensity', win_name=self.windowName)
            ret, frame = self.cap.read()
            returned_frame = self.effectRunner.runEffect(self.mode, frame, param)
            cv2.imwrite(f'./image_{now.strftime("%d-%m-%Y_%H_%M_%S")}.jpg', returned_frame)
        else :
            self.mode = mode

    def make_slider(self, min: int, max: int, default: int, slider_id: str, win_name: str) -> str:
        """Function to easily make slider gui element

        Parameters
        ----------
        min : int
            minimum slider value
        max : int
            maximum slider value
        default : int
            default slider value
        slider_id : str
            name of slider
        win_name : str
            name of window that slider will exist in

        Returns
        -------
        str
            the slider_id of the slider created
        """

        cv2.createTrackbar(slider_id, win_name, min, max, lambda x: x)
        cv2.setTrackbarPos(slider_id, win_name, default)
        return slider_id

    def get_slider(self, *ids, win_name: str) :
        """Gets a series of trackbar positions given a list of trackbar objects

        Parameters
        ----------
        *ids :
            the list holding the trackbar id's. or single slider_id
        root_wind : str
            window name that the trackbars sit in

        Returns
        -------
            array of ints:
                list of trackbar positions, or single slider_id
        """

        try:
            results = [cv2.getTrackbarPos(idd, win_name) for idd in ids]
            return results[0] if len(results) == 1 else results
        except Exception as e:
            print(f'Error in fetching slider value - {str(e)}')
            return None

    def set_slider(slider_id: str, value: int, win_name: str):
        """Sets a slider position given an id

        Parameters
        ----------
        slider_id : str
            slider_id of trackbar to set
        value : int
            value to set trackbar to
        win_name : str
            window name where trackbar exists
        """
        
        cv2.setTrackbarPos(slider_id, win_name, value)