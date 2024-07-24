import sys
import os
import glob
import os.path
import sqlite3
import shutil
import time



from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QScrollArea, QCheckBox, \
    QGridLayout, QHBoxLayout, QVBoxLayout, QMenuBar, QAction, QLineEdit


class ErrorWindow(QWidget):
    def __init__(self, Error):
        super().__init__()
        uic.loadUi('bin/Windows/ErrorForm.ui', self)
        self.Number = Error
        self.initUi()

    def initUi(self):
        self.OkButton.clicked.connect(self.close)
        if self.Number == 101:
            self.ErrorLable.setText('Error 101: Папка не выбрана!')
        elif self.Number == 102:
            self.ErrorLable.setText('Error 102: База данных отсутствует!')
        elif self.Number == 201:
            self.ErrorLable.setText('Error 201: Удалите знаки из формата!')
