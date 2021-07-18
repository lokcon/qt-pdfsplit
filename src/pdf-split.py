#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyPdf import PdfFileWriter, PdfFileReader
from PySide.QtGui import *
from PySide.QtCore import *
import sys

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 100
APP_NAME = u'PDF Split'

###############################################################
## Main
###############################################################

class mainWindow(QMainWindow):
    def __init__(self, dimension):
        QMainWindow.__init__(self)


        self.file_line_edit = QLineEdit()
        self.file_line_edit.setReadOnly(True)
        file_button = QPushButton(u'Open File')
        file_button.clicked.connect(self.openFile)

        fileLayout = QHBoxLayout()
        fileLayout.addWidget(QLabel(u'File: '))
        fileLayout.addWidget(self.file_line_edit)
        fileLayout.addWidget(file_button)


        self.pages_line_edit = QLineEdit()
        self.pages_line_edit.setPlaceholderText(u'e.g. 1-3,4,7-8,10,13')
        self.output_button = QPushButton(u'Export')
        self.output_button.setEnabled(False)
        self.output_button.clicked.connect(self.output)

        pagesLayout = QHBoxLayout()
        pagesLayout.addWidget(QLabel(u'Pages: '))
        pagesLayout.addWidget(self.pages_line_edit)
        pagesLayout.addWidget(self.output_button)



        mainLayout = QVBoxLayout()
        mainLayout.addLayout(fileLayout)
        mainLayout.addLayout(pagesLayout)


        # Centre the web window to the screen
        desktop = QApplication.desktop()
        screen = desktop.screenGeometry(desktop.primaryScreen())
        (width, height) = dimension

        pos_x = (screen.width() - width)/2 + screen.left()
        pos_y = (screen.height() - height)/2 + screen.top()
        self.setWindowTitle(APP_NAME)
        self.setGeometry(pos_x, pos_y, width, height)

        # Main window set-up
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        self.show()

        # set focus to the openfile button
        file_button.setFocus()


    @Slot()
    def openFile(self):
        (self.in_filename, filter) = \
            QFileDialog.getOpenFileName(parent = self,
                                        caption = self.tr(u'Open'),
                                        dir = '',
                                        filter = self.tr('pdf (*.pdf)'))

        # update the line edit
        self.file_line_edit.setText(self.in_filename)

        # enable the output button
        self.output_button.setEnabled(True)

    @Slot()
    def output(self):
        # get the output filename using the file dialog
        (out_filename, filter) = \
            QFileDialog.getSaveFileName(parent = self,
                                        caption = self.tr(u'Export'),
                                        dir = '',
                                        filter = self.tr('pdf (*.pdf)'))

        # file IO
        out_file = open(out_filename, 'wb')
        in_file = open(self.in_filename, 'rb')
        in_reader = PdfFileReader(in_file)
        out_writer = PdfFileWriter()

        # extract input
        pages_string = self.pages_line_edit.text()

        # Get the indices of pages  to extract
        pages = pages_parser(in_reader.getNumPages()).parse(pages_string)

        # append pages to output writer
        for page_index in pages:
            out_writer.addPage(in_reader.getPage(page_index))

        # write to file
        out_writer.write(out_file)

        # close files
        in_file.close()
        out_file.close()


class pages_parser():
    def __init__(self, num_pages):
        self.num_pages = num_pages

    def parse(self, in_string):
        clean_string = pages_parser.remove_spaces(in_string)

        out_pages = []
        for fragment in clean_string.split(','):
            if '-' in fragment:
                (start, end) = fragment.split('-')
                for index in range(int(start) - 1 , int(end)):
                    out_pages.append(index)
            else:
                out_pages.append(int(fragment) - 1)

        filtered_pages = [page for page in out_pages if page < self.num_pages]

        return filtered_pages


    @staticmethod
    def remove_spaces(in_string):
        return ''.join(in_string.split())


def main():
    main_app = QApplication(sys.argv)
    main_window = mainWindow(dimension = (WINDOW_WIDTH, WINDOW_HEIGHT))
    main_app.exec_()


if __name__ == '__main__':
    main()
