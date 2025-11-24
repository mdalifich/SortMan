import sys
import os
import glob
import os.path
import sqlite3
import shutil
import time

import bin.FormatsWindowClass
from bin.FormatsWindowClass import *

import bin.ErrorWindowClass
from bin.ErrorWindowClass import *


from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QScrollArea, QCheckBox, \
    QGridLayout, QHBoxLayout, QVBoxLayout, QMenuBar, QAction, QLineEdit


class SortMain(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('bin/Windows/SortWindow.ui', self)