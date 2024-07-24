import sys
import os
import glob
import os.path
import sqlite3
import shutil
import time
import bin.MainWindowClass
from bin.MainWindowClass import *

from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QScrollArea, QCheckBox, \
    QGridLayout, QHBoxLayout, QVBoxLayout, QMenuBar, QAction, QLineEdit


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SortMain()
    ex.show()
    sys.exit(app.exec())
