import logging
import sys
from tkinter import Tk
from commonfunc import CommonDataFunction
from calculatorgui import RentalCalculatorGUI

rootWindow = Tk()


def mainFunction():
    commonObj = CommonDataFunction()
    # Setting logger for all Classes
    try:
        logFileName = commonObj.setLoggingFile()
        logger = logging.getLogger('calculator-logger')
    except Exception as e:
        print('Not able to set application logging. Exiting. ', e)
        sys.exit()
    RentalCalculatorGUI(rootWindow, logFileName)
    rootWindow.protocol('WM_DELETE_WINDOW', windowClose)
    rootWindow.mainloop()


def windowClose():
    """
    Close GUI window.
    """
    print('Closing Window')
    rootWindow.destroy()
    sys.exit()


if __name__ == '__main__':
    mainFunction()