import logging
from tkinter import E, END, FALSE, N, S, W
from tkinter import Label, Text, ttk
from tkinter import StringVar, IntVar
from tkinter.constants import DISABLED, NORMAL
from tkinter.font import nametofont


class RentalCalculatorGUI:
    def __init__(self, master, logFileName):
        self.master = master
        self.logFileName = logFileName
        self.logger = logging.getLogger('calculator-logger')
        self.note = None
        self.userFrame = None
        self.logFileLabelGroup = None
        self.logFileLabel = None
        self.optionsSelectGroup = None
        self.framesList = {}
        self.logFileDestination = StringVar()

        self.master.title('Rental Calculator')
        self.createUIVariables()
        self.createWidgets()
        self.default_font = nametofont('TkDefaultFont')
        self.default_font.configure(size=12)
        self.master.option_add('*Font', self.default_font)
        self.style = ttk.Style()
        self.style.configure(
            'red.Horizontal.TProgressbar',
            foreground='#000000',
            troughcolor='#fff',
            background='blue',
        )

    def createUIVariables(self):
        self.logFileDestination.set(self.logFileName)

    def createWidgets(self):
        self.logger.info('Starting UI.')
        self.master.option_add('*tearOff', FALSE)
        self.note = ttk.Notebook(self.master)
        self.userSelect()
        self.finalizeUI()

    def userSelect(self):
        # Frame
        self.userFrame = ttk.Frame(self.note)
        self.framesList['USER'] = self.userFrame
        self.userFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.userFrame.columnconfigure(0, weight=2)

        # Log File
        self.logFileLabelGroup = ttk.Labelframe(self.userFrame, text='Log File')
        self.logFileLabelGroup.grid(row=0)
        self.logFileLabel = Label(
            self.logFileLabelGroup, textvariable=self.logFileDestination
        )
        self.logFileLabel.grid(row=1, padx=10, pady=10)

        self.optionsSelectGroup = ttk.LabelFrame(self.userFrame, text='Select Appropriate Options')
        self.optionsSelectGroup.grid(row=1)

    def finalizeUI(self):
        """
        Finalize the GUI elements.
        """
        for frameName, frameObj in self.framesList.items():
            self.padFrameWidgets(frameObj)
        for frameName, frameObj in self.framesList.items():
            self.note.add(frameObj, text=frameName)
        self.note.pack()
        ttk.Style().theme_use('alt')

    @staticmethod
    def padFrameWidgets(inputFrame):
        """
        Set padding for the input frame.
        :param inputFrame: input frame
        """
        for child in inputFrame.winfo_children():
            child.grid_configure(padx=10, pady=10)
