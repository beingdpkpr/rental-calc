import logging
import os


class CommonDataFunction:
    def __init__(self):
        self.logger = None

    def setLoggingFile(self):
        """
        Set logger file for the app.
        :return: log file name
        """
        self.logger = logging.getLogger('calculator-logger')
        self.logger.setLevel(logging.DEBUG)
        fileNameForLogging = os.path.join(os.getcwd(), 'rental-calculator.log')
        print('setting log file to ' + fileNameForLogging)
        # Open file and overwrite it to empty it
        open(fileNameForLogging, 'w').close()
        fh = logging.FileHandler(fileNameForLogging)
        fh.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        # Remove existing handlers if any
        for fHandler in self.logger.handlers:
            print('Removing existing file log handler')
            self.logger.removeHandler(fHandler)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.info('Logger Initialized')
        return fileNameForLogging
