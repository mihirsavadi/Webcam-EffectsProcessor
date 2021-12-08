from lib import *
import gui.gui

if __name__ == '__main__' :

    mainGui = gui.gui.guiClass("ECE4580 Final Project: Webcam Effects")

    # run event loop
    while True:

        mainGui.eventLoop()

        # if 'q' key hit then quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()