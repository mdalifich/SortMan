import sys
import os
import glob
import os.path
import sqlite3
import shutil
import time

from bin.ErrorWindowClass import *

from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QScrollArea, QCheckBox, \
    QGridLayout, QHBoxLayout, QVBoxLayout, QMenuBar, QAction, QLineEdit

class dialugueWindow(QWidget):
    def __init__(self, Type):
        super().__init__()
        self.TypeDialogue = Type
        self.initUi()

    def initUi(self):
        self.error = ErrorWindow(201)
        #
        self.setGeometry(200, 200, 200, 110)
        self.setWindowTitle(self.TypeDialogue)
        #
        self.OkButton = QPushButton(self)
        self.OkButton.setText('OK')
        self.OkButton.move(0, 40)
        self.OkButton.resize(200, 31)
        self.OkButton.clicked.connect(self.OkClick)
        #
        self.CancelButton = QPushButton(self)
        self.CancelButton.setText('Отмена')
        self.CancelButton.move(0, 80)
        self.CancelButton.resize(200, 31)
        self.CancelButton.clicked.connect(self.Cancel)
        #
        self.Logs = QLineEdit(self)
        self.Logs.move(0, 2)
        self.Logs.resize(200, 31)
        if self.TypeDialogue == 'Удалить':
            self.Logs.setEnabled(False)
            self.Logs.setText('Удалить выбранные типы?')

    def OkClick(self):
        flag = True
        if self.TypeDialogue == 'Добавить':
            for i in self.Logs.text():
                if i in ".,'\"@#$%^&*()!~?:|\\/{}[]/*-+:,.;?%_+|><`¤":
                    flag = False
                else:
                    self.error.show()
            if flag:
                self.OpenDataBase()
                chekBaseInfo = f'INSERT INTO FormatFile(Format, Chek) VALUES ("{self.Logs.text()}", 0) '
                self.curs.execute(chekBaseInfo).fetchall()
                self.CloseDataBase()

        elif self.TypeDialogue == 'Удалить':
            self.OpenDataBase()
            chekBaseInfo = f'DELETE FROM FormatFile WHERE Chek == 1'
            self.curs.execute(chekBaseInfo).fetchall()
            self.CloseDataBase()
        if flag:
            self.close()


    def OpenDataBase(self):
        self.DataBase = sqlite3.connect('bin/DataBase/BD.sqlite')
        self.curs = self.DataBase.cursor()

    def CloseDataBase(self):
        self.DataBase.commit()
        self.DataBase.close()

    def Cancel(self):
        self.close()