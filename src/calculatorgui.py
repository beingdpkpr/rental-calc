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
        self.carTypeCombobox = None
        self.carTypeLabel = None
        self.calculateRentalButton = None
        self.calculatedRentalGrp = None
        self.calculatedRentalLabel = None
        self.framesList = {}
        self.logFileDestination = StringVar()
        self.carTypeDropDown = StringVar()
        self.resultString = StringVar()
        self.carTypeList = ['Type1', 'Type2']

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
        self.carTypeDropDown.set('')
        self.resultString.set('RESULT')

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

        # Select options.
        self.optionsSelectGroup = ttk.Labelframe(
            self.userFrame, text='Select Appropriate Options'
        )
        self.optionsSelectGroup.grid(row=1)
        self.carTypeLabel = Label(self.optionsSelectGroup, text='Car Type:')
        self.carTypeLabel.grid(row=0, column=0, padx=10, pady=10)
        font = ('TkDefaultFont', '12')
        self.carTypeCombobox = ttk.Combobox(
            self.optionsSelectGroup,
            state='readonly',
            font=font,
            width=45,
            textvariable=self.carTypeDropDown,
        )
        self.carTypeCombobox.grid(row=0, column=1, padx=10, pady=10)
        self.carTypeCombobox['values'] = self.carTypeList

        self.calculateRentalButton = ttk.Button(
            self.userFrame,
            text='Calculate Rental',
            command=self.calculateRentalButtonClick,
        )
        self.calculateRentalButton.grid(row=10)

        self.calculatedRentalGrp = ttk.Labelframe(self.userFrame, text='Calculated Rental')
        self.calculatedRentalGrp.grid(row=12)
        self.calculatedRentalLabel = Label(self.calculatedRentalGrp, text=self.resultString.get())
        self.calculatedRentalLabel.grid(row=0)
        self.disable(self.calculatedRentalGrp)
        # self.calculatedRentalGrp.grid_remove()

    def calculateRentalButtonClick(self):
        print('---', self.carTypeDropDown.get())
        self.enable(self.calculatedRentalGrp)

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

    @staticmethod
    def enable(frame):
        for child in frame.winfo_children():
            child.grid()

    @staticmethod
    def disable(frame):
        for child in frame.winfo_children():
            child.grid_remove()