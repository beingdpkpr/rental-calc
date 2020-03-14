import os
import logging
from tkinter import E, END, FALSE, N, S, W
from tkinter import Label, Text, ttk, filedialog
from tkinter import StringVar, IntVar
from tkinter.constants import DISABLED, NORMAL
from tkinter.font import nametofont
from pandas import read_csv


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
        self.millageCombobox = None
        self.carTypeCombobox = None
        self.millageLabel = None
        self.rvCombobox = None
        self.rvLabel = None
        self.tenureCombobox = None
        self.carTypeLabel = None
        self.calculateRentalButton = None
        self.calculatedRentalGrp = None
        self.calculatedRentalLabel = None
        self.statusLabelForFileFrame = None
        self.inputData = None
        self.selectFileGroup = None
        self.chooseFileButton = None
        self.inputFileLabel = None
        self.tenureLabel = None
        self.framesList = {}
        self.logFileDestination = StringVar()
        self.carTypeDropDown = StringVar()
        self.tenureDropDown = StringVar()
        self.millageDropDown = StringVar()
        self.rvTypeDropDown = StringVar()
        self.resultString = StringVar()
        self.csvFile = StringVar()
        self.appStatus = StringVar()

        self.carTypeList = []
        self.tenureList = []
        self.millageList = []
        self.RVList = []

        self.master.title('Rental Calculator')
        self.createUIVariables()
        self.createWidgets()
        self.calculateRentalButton.configure(state=DISABLED)
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
        self.millageDropDown.set('')
        self.tenureDropDown.set('')
        self.rvTypeDropDown.set('')
        self.resultString.set('NA')
        self.csvFile.set('')
        self.appStatus.set('')

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

        # GetFile
        self.selectFileGroup = ttk.Labelframe(
            self.userFrame, text='Input File'
        )
        self.selectFileGroup.grid(row=1)
        self.chooseFileButton = ttk.Button(
            self.selectFileGroup, text='Choose Input CSV File', command=self.chooseInputFileClicked
        )
        self.chooseFileButton.grid(row=0)
        self.inputFileLabel = Label(self.selectFileGroup, textvariable=self.csvFile)
        self.inputFileLabel.grid(row=1)

        # Select options.
        self.optionsSelectGroup = ttk.Labelframe(
            self.userFrame, text='Select Appropriate Options'
        )
        self.optionsSelectGroup.grid(row=2)
        self.carTypeLabel = Label(self.optionsSelectGroup, text='Car Model:')
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

        self.tenureLabel = Label(self.optionsSelectGroup, text='Tenure:')
        self.tenureLabel.grid(row=1, column=0, padx=10, pady=10)

        self.tenureCombobox = ttk.Combobox(
            self.optionsSelectGroup,
            state='readonly',
            font=font,
            width=45,
            textvariable=self.tenureDropDown,
        )
        self.tenureCombobox.grid(row=1, column=1, padx=10, pady=10)
        self.tenureCombobox['values'] = self.tenureList

        self.millageLabel = Label(self.optionsSelectGroup, text='Millage:')
        self.millageLabel.grid(row=2, column=0, padx=10, pady=10)

        self.millageCombobox = ttk.Combobox(
            self.optionsSelectGroup,
            state='readonly',
            font=font,
            width=45,
            textvariable=self.millageDropDown,
        )
        self.millageCombobox.grid(row=2, column=1, padx=10, pady=10)
        self.millageCombobox['values'] = self.millageList

        self.rvLabel = Label(self.optionsSelectGroup, text='RV:')
        self.rvLabel.grid(row=3, column=0, padx=10, pady=10)

        self.rvCombobox = ttk.Combobox(
            self.optionsSelectGroup,
            state='readonly',
            font=font,
            width=45,
            textvariable=self.rvTypeDropDown,
        )
        self.rvCombobox.grid(row=3, column=1, padx=10, pady=10)
        self.rvCombobox['values'] = self.millageList

        self.calculateRentalButton = ttk.Button(
            self.userFrame,
            text='Calculate Rental',
            command=self.calculateRentalButtonClick,
        )
        self.calculateRentalButton.grid(row=10)

        self.calculatedRentalGrp = ttk.Labelframe(self.userFrame, text='Calculated Rental')
        self.calculatedRentalGrp.grid(row=12)
        self.calculatedRentalLabel = Label(self.calculatedRentalGrp, textvariable=self.resultString)
        self.calculatedRentalLabel.grid(row=0)
        self.disable(self.calculatedRentalGrp)

        self.statusLabelForFileFrame = Label(
            self.userFrame, textvariable=self.appStatus
        )
        self.statusLabelForFileFrame.grid(row=20)

    def chooseInputFileClicked(self):
        self.calculateRentalButton.configure(state=DISABLED)
        filePath = filedialog.askopenfilename()
        self.csvFile.set(filePath)
        if not os.path.isfile(self.csvFile.get()):
            self.updateStatus('Input file not chosen.', 'yellow')
            return
        else:
            self.updateStatus('Input file selected.')
            self.getDataFromInputFile()

    def getDataFromInputFile(self):
        self.inputData = read_csv(self.csvFile.get())
        if len(self.inputData) < 1:
            self.updateStatus('Empty Input File', 'red')
        self.carTypeList = list(self.inputData.Model.unique())
        self.millageList = list(self.inputData.Millage.unique())
        self.tenureList = list(self.inputData.Tenure.unique())
        self.RVList = list(self.inputData.RVType.unique())
        self.carTypeCombobox['values'] = self.carTypeList
        self.tenureCombobox['values'] = self.tenureList
        self.millageCombobox['values'] = self.millageList
        self.rvCombobox['values'] = self.RVList
        self.calculateRentalButton.configure(state=NORMAL)

    def calculateRentalButtonClick(self):
        # print('---', self.carTypeDropDown.get())
        if self.carTypeDropDown.get() != '':
            if self.tenureDropDown.get() != '':
                if self.millageDropDown.get() != '':
                    if self.rvTypeDropDown.get() != '':
                        header = ['Model', 'Tenure', 'Millage', 'RVType']
                        value = [self.carTypeDropDown.get(), int(self.tenureDropDown.get()), int(self.millageDropDown.get()), self.rvTypeDropDown.get()]

                        match = self.inputData[self.inputData[header] == value]
                        finalIndex = match[header].dropna().index.tolist()
                        if len(finalIndex) < 0:
                            self.updateStatus('No Data with this values.')
                        else:
                            self.resultString.set(str(self.inputData.iloc[finalIndex[0]]['Amount']))
                            print('---', self.inputData.iloc[finalIndex[0]]['Amount'])
                            print(self.resultString.get())
                        self.updateStatus('Result Fetching.')

                        self.enable(self.calculatedRentalGrp)
                    else:
                        self.updateStatus('Select RV Type.', 'red')
                else:
                    self.updateStatus('Select Millage.', 'red')
            else:
                self.updateStatus('Select Tenure.', 'red')
            # self.enable(self.calculatedRentalGrp)
        else:
            self.updateStatus('Select Car Model.', 'red')
            print('Select all options.')

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

    def updateStatus(self, updateText, color='sky blue'):
        self.appStatus.set(updateText)
        self.statusLabelForFileFrame.configure(bg=color)
